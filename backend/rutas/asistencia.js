
const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();

// ============================================================
// AGREGAR UNA ASISTENCIA
// POST /asistencia
// ============================================================

router.post('/', async (req, res) => {
    try {
        const {
            curso,
            fecha,
            estado,
            motivo_justificacion,
            id_estudiante
        } = req.body;

        const sql = `
            INSERT INTO asistencias
            (curso, fecha, estado, motivo_justificacion, id_estudiante)
            VALUES (?, ?, ?, ?, ?)
        `;

        const [resultado] = await pool.execute(sql, [
            curso,
            fecha,
            estado,
            motivo_justificacion || '',
            id_estudiante
        ]);

        res.status(201).json({
            mensaje: 'Asistencia agregada correctamente',
            id: resultado.insertId
        });

    } catch (error) {
        res.status(500).json({
            error: 'No se pudo agregar la asistencia',
            detalle: error.message
        });
    }
});


// ============================================================
// LISTAR TODAS LAS ASISTENCIAS
// GET /asistencia
// ============================================================

router.get('/', async (req, res) => {
    try {
        const sql = `
            SELECT *
            FROM asistencias
            ORDER BY fecha DESC
        `;

        const [resultado] = await pool.execute(sql);

        res.json(resultado);

    } catch (error) {
        res.status(500).json({
            error: 'No se pudieron obtener las asistencias',
            detalle: error.message
        });
    }
});


// ============================================================
// BUSCAR UNA ASISTENCIA POR ID
// GET /asistencia/:id
// ============================================================

router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const sql = `
            SELECT *
            FROM asistencias
            WHERE id_asistencia = ?
        `;

        const [resultado] = await pool.execute(sql, [id]);

        if (resultado.length === 0) {
            return res.status(404).json({
                error: 'No se encontró la asistencia'
            });
        }

        res.json(resultado[0]);

    } catch (error) {
        res.status(500).json({
            error: 'No se pudo obtener la asistencia',
            detalle: error.message
        });
    }
});


// ============================================================
// MODIFICAR UNA ASISTENCIA
// PUT /asistencia/:id
// Permite modificar solamente los campos enviados
// ============================================================

router.put('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const camposPermitidos = [
            'curso',
            'fecha',
            'estado',
            'motivo_justificacion',
            'id_estudiante'
        ];

        const campos = [];
        const valores = [];

        // Verificar que exista la asistencia
        const [asistencia] = await pool.execute(
            'SELECT * FROM asistencias WHERE id_asistencia = ?',
            [id]
        );

        if (asistencia.length === 0) {
            return res.status(404).json({
                error: 'No se encontró la asistencia'
            });
        }

        // Validar el estado si se envía
        if (req.body.estado !== undefined) {
            const estadosPermitidos = [
                'Presente',
                'Tardanza',
                'Falta',
                'Ausente'
            ];

            if (!estadosPermitidos.includes(req.body.estado)) {
                return res.status(400).json({
                    error: 'El estado de asistencia no es válido'
                });
            }
        }

        // Construir la actualización solamente con los campos enviados
        for (const campo of camposPermitidos) {
            if (req.body[campo] !== undefined) {
                campos.push(`${campo} = ?`);
                valores.push(req.body[campo]);
            }
        }

        if (campos.length === 0) {
            return res.status(400).json({
                error: 'No se enviaron datos para modificar'
            });
        }

        valores.push(id);

        const sql = `
            UPDATE asistencias
            SET ${campos.join(', ')}
            WHERE id_asistencia = ?
        `;

        await pool.execute(sql, valores);

        res.json({
            mensaje: 'Asistencia modificada correctamente'
        });

    } catch (error) {
        res.status(500).json({
            error: 'No se pudo modificar la asistencia',
            detalle: error.message
        });
    }
});


// ============================================================
// ELIMINAR UNA ASISTENCIA
// DELETE /asistencia/:id
// ============================================================

router.delete('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const [resultado] = await pool.execute(
            'DELETE FROM asistencias WHERE id_asistencia = ?',
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'No se encontró la asistencia'
            });
        }

        res.json({
            mensaje: 'Asistencia eliminada correctamente'
        });

    } catch (error) {
        res.status(500).json({
            error: 'No se pudo eliminar la asistencia',
            detalle: error.message
        });
    }
});


// ============================================================
// EXPORTAR RUTAS
// ============================================================

module.exports = router;
