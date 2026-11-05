
const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();

// ======================================================
// CONFIGURACIÓN GENERAL
// ======================================================

// Cantidad mínima de inasistencias para generar una alerta.
const UMBRAL_DEFAULT = 3;

// IMPORTANTE:
// Estos estados deben coincidir con los valores
// que guardás realmente en la columna asistencias.estado.

const ESTADOS_ASISTENCIA = [
    'presente',
    'asistencia',
    'asistio',
    'asistió'
];

const ESTADOS_INASISTENCIA = [
    'ausente',
    'inasistencia',
    'ausencia',
    'falta'
];

// ======================================================
// FUNCIONES AUXILIARES
// ======================================================

function normalizarEstado(estado) {
    return String(estado || '').trim().toLowerCase();
}

function validarFecha(fecha) {
    if (!fecha) return true;

    if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha)) {
        return false;
    }

    const [anio, mes, dia] = fecha.split('-').map(Number);
    const fechaReal = new Date(Date.UTC(anio, mes - 1, dia));

    return fechaReal.getUTCFullYear() === anio &&
        fechaReal.getUTCMonth() === mes - 1 &&
        fechaReal.getUTCDate() === dia;
}

// Prepara los filtros que se pueden utilizar
// en las consultas de asistencia.

function obtenerFiltros(query) {
    const { desde, hasta, curso, id_estudiante } = query;

    if (!validarFecha(desde) || !validarFecha(hasta)) {
        throw new Error(
            'Las fechas deben tener formato YYYY-MM-DD'
        );
    }

    if (desde && hasta && desde > hasta) {
        throw new Error(
            'La fecha inicial no puede ser posterior a la final'
        );
    }

    const condiciones = [];
    const valores = [];

    if (desde) {
        condiciones.push('a.fecha >= ?');
        valores.push(desde);
    }

    if (hasta) {
        condiciones.push('a.fecha <= ?');
        valores.push(hasta);
    }

    if (curso) {
        condiciones.push('a.curso = ?');
        valores.push(curso);
    }

    if (
        id_estudiante !== undefined &&
        id_estudiante !== ''
    ) {
        if (!/^\d+$/.test(String(id_estudiante))) {
            throw new Error(
                'El ID del estudiante debe ser numérico'
            );
        }

        condiciones.push('a.id_estudiante = ?');
        valores.push(Number(id_estudiante));
    }

    return {
        sql: condiciones.length
            ? 'WHERE ' + condiciones.join(' AND ')
            : '',
        valores
    };
}

// ======================================================
// 1. RESUMEN GENERAL DEL PANEL
// GET /api/dashboard/resumen
// ======================================================

router.get('/resumen', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const [[estudiantes]] = await pool.execute(`
            SELECT COUNT(*) AS total
            FROM estudiantes
        `);

        const [[asistencias]] = await pool.execute(`
            SELECT
                COUNT(*) AS total_registros,

                COALESCE(SUM(
                    CASE
                        WHEN LOWER(TRIM(a.estado)) IN
                        ('ausente', 'inasistencia', 'ausencia', 'falta')
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS total_inasistencias

            FROM asistencias a
            ${filtros.sql}
        `, filtros.valores);

        const [[observaciones]] = await pool.execute(`
            SELECT COUNT(*) AS total
            FROM observaciones
            WHERE LOWER(TRIM(requiere_seguimiento))
                IN ('si', 'sí', 's', '1')
        `);

        const totalRegistros = Number(asistencias.total_registros);
        const totalInasistencias =
            Number(asistencias.total_inasistencias);

        res.json({
            total_estudiantes: Number(estudiantes.total),

            registros_asistencia: totalRegistros,

            inasistencias: totalInasistencias,

            porcentaje_inasistencias: totalRegistros > 0
                ? Number((
                    totalInasistencias /
                    totalRegistros * 100
                ).toFixed(2))
                : 0,

            observaciones_pendientes:
                Number(observaciones.total)
        });

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

// ======================================================
// 2. ALERTAS DE INASISTENCIAS
// GET /api/dashboard/alertas
// GET /api/dashboard/alertas?umbral=5
// ======================================================

router.get('/alertas', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const umbral = req.query.umbral === undefined
            ? UMBRAL_DEFAULT
            : Number(req.query.umbral);

        if (
            !Number.isInteger(umbral) ||
            umbral < 1 ||
            umbral > 365
        ) {
            return res.status(400).json({
                error: 'El umbral debe ser un entero entre 1 y 365'
            });
        }

        const [filas] = await pool.execute(`
            SELECT
                e.id_estudiante,
                e.nombre,
                e.apellido,
                a.curso,

                COUNT(*) AS total_registros,

                SUM(
                    CASE
                        WHEN LOWER(TRIM(a.estado)) IN
                        ('ausente', 'inasistencia', 'ausencia', 'falta')
                        THEN 1
                        ELSE 0
                    END
                ) AS cantidad_inasistencias,

                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN LOWER(TRIM(a.estado)) IN
                            ('ausente', 'inasistencia', 'ausencia', 'falta')
                            THEN 1
                            ELSE 0
                        END
                    ) / NULLIF(COUNT(*), 0),
                    2
                ) AS porcentaje_inasistencias

            FROM asistencias a

            INNER JOIN estudiantes e
                ON e.id_estudiante = a.id_estudiante

            ${filtros.sql}

            GROUP BY
                e.id_estudiante,
                e.nombre,
                e.apellido,
                a.curso

            HAVING cantidad_inasistencias >= ?

            ORDER BY
                cantidad_inasistencias DESC,
                e.apellido ASC
        `, [...filtros.valores, umbral]);

        res.json({
            umbral,
            total_alertas: filas.length,
            alertas: filas
        });

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

// ======================================================
// 3. GRÁFICO DE ASISTENCIAS POR CURSO
// GET /api/dashboard/por-curso
// ======================================================

router.get('/por-curso', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const [filas] = await pool.execute(`
            SELECT
                a.curso,

                COUNT(*) AS total_registros,

                SUM(
                    CASE
                        WHEN LOWER(TRIM(a.estado)) IN
                        ('presente', 'asistencia', 'asistio', 'asistió')
                        THEN 1
                        ELSE 0
                    END
                ) AS asistencias,

                SUM(
                    CASE
                        WHEN LOWER(TRIM(a.estado)) IN
                        ('ausente', 'inasistencia', 'ausencia', 'falta')
                        THEN 1
                        ELSE 0
                    END
                ) AS inasistencias

            FROM asistencias a

            ${filtros.sql}

            GROUP BY a.curso
            ORDER BY a.curso ASC
        `, filtros.valores);

        res.json(filas);

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

// ======================================================
// 4. EVOLUCIÓN MENSUAL DE INASISTENCIAS
// GET /api/dashboard/evolucion-mensual
// ======================================================

router.get('/evolucion-mensual', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const [filas] = await pool.execute(`
            SELECT
                DATE_FORMAT(a.fecha, '%Y-%m') AS mes,

                COUNT(*) AS total_registros,

                SUM(
                    CASE
                        WHEN LOWER(TRIM(a.estado)) IN
                        ('ausente', 'inasistencia', 'ausencia', 'falta')
                        THEN 1
                        ELSE 0
                    END
                ) AS inasistencias

            FROM asistencias a

            ${filtros.sql}

            GROUP BY DATE_FORMAT(a.fecha, '%Y-%m')
            ORDER BY mes ASC
        `, filtros.valores);

        res.json(filas);

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

// ======================================================
// 5. OBSERVACIONES QUE REQUIEREN SEGUIMIENTO
// GET /api/dashboard/observaciones
// ======================================================

router.get('/observaciones', async (req, res) => {
    try {
        const [filas] = await pool.execute(`
            SELECT
                o.id_observacion,
                o.fecha,
                o.tipo,
                o.descripcion,
                o.requiere_seguimiento,

                e.id_estudiante,
                e.nombre AS nombre_estudiante,
                e.apellido AS apellido_estudiante,

                d.id_docente,
                d.nombre AS nombre_docente,
                d.apellido AS apellido_docente

            FROM observaciones o

            INNER JOIN estudiantes e
                ON e.id_estudiante = o.id_estudiante

            INNER JOIN docentes d
                ON d.id_docente = o.id_docente

            WHERE LOWER(TRIM(o.requiere_seguimiento))
                IN ('si', 'sí', 's', '1')

            ORDER BY o.fecha DESC, o.id_observacion DESC
        `);

        res.json({
            total: filas.length,
            observaciones: filas
        });

    } catch (error) {
        res.status(500).json({
            error: 'Error al consultar las observaciones',
            detalle: error.message
        });
    }
});

// ======================================================
// 6. INFORME DE ASISTENCIA
// GET /api/dashboard/informe
//
// Filtros opcionales:
// ?desde=2026-03-01
// ?hasta=2026-03-31
// ?curso=1A
// ?id_estudiante=1
// ======================================================

router.get('/informe', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const [filas] = await pool.execute(`
            SELECT
                a.id_asistencia,
                a.fecha,
                a.curso,
                a.estado,
                a.motivo_justificacion,

                e.id_estudiante,
                e.nombre,
                e.apellido,
                e.dni

            FROM asistencias a

            INNER JOIN estudiantes e
                ON e.id_estudiante = a.id_estudiante

            ${filtros.sql}

            ORDER BY a.fecha DESC, e.apellido ASC
        `, filtros.valores);

        res.json({
            total_registros: filas.length,
            registros: filas
        });

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

// ======================================================
// 7. DESCARGAR INFORME EN CSV
// GET /api/dashboard/informe/csv
// ======================================================

router.get('/informe/csv', async (req, res) => {
    try {
        const filtros = obtenerFiltros(req.query);

        const [filas] = await pool.execute(`
            SELECT
                a.fecha,
                a.curso,
                e.id_estudiante,
                e.nombre,
                e.apellido,
                e.dni,
                a.estado,
                a.motivo_justificacion

            FROM asistencias a

            INNER JOIN estudiantes e
                ON e.id_estudiante = a.id_estudiante

            ${filtros.sql}

            ORDER BY a.fecha DESC, e.apellido ASC
        `, filtros.valores);

        const columnas = [
            'Fecha',
            'Curso',
            'ID estudiante',
            'Nombre',
            'Apellido',
            'DNI',
            'Estado',
            'Motivo de justificación'
        ];

        function escaparCSV(valor) {
            let texto = valor == null ? '' : String(valor);

            // Evita interpretar texto como fórmula al abrir
            // el archivo en programas de hojas de cálculo.
            if (/^[\s]*[=+\-@]/.test(texto)) {
                texto = "'" + texto;
            }

            return '"' + texto.replace(/"/g, '""') + '"';
        }

        const lineas = [
            columnas.map(escaparCSV).join(';'),

            ...filas.map(fila => [
                fila.fecha,
                fila.curso,
                fila.id_estudiante,
                fila.nombre,
                fila.apellido,
                fila.dni,
                fila.estado,
                fila.motivo_justificacion
            ].map(escaparCSV).join(';'))
        ];

        const contenido = '\uFEFF' + lineas.join('\r\n');

        res.setHeader(
            'Content-Type',
            'text/csv; charset=utf-8'
        );

        res.setHeader(
            'Content-Disposition',
            'attachment; filename="informe_asistencia.csv"'
        );

        res.send(contenido);

    } catch (error) {
        res.status(400).json({
            error: error.message
        });
    }
});

module.exports = router;
