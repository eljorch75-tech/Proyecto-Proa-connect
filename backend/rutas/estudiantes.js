
const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();

// ===============================
// AGREGAR UN ESTUDIANTE
// POST /estudiantes
// ===============================
router.post('/', async (req, res) => {
    const {
        nombre,
        apellido,
        dni,
        fecha_nacimiento,
        nombre_tutor,
        telefono_tutor,
        email_tutor,
        id_curso
    } = req.body;

    // Validar que se haya seleccionado un curso
    if (id_curso === undefined || id_curso === null || id_curso === '') {
        return res.status(400).json({
            error: 'El curso es obligatorio'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO estudiantes
            (
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                nombre_tutor,
                telefono_tutor,
                email_tutor,
                id_curso
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                nombre_tutor,
                telefono_tutor,
                email_tutor,
                id_curso
            ]
        );

        return res.status(201).json({
            mensaje: 'Estudiante agregado correctamente',
            id: resultado.insertId,
            id_curso: Number(id_curso)
        });

    } catch (error) {
        if (error.code === 'ER_NO_REFERENCED_ROW_2') {
            return res.status(400).json({
                error: 'El curso seleccionado no existe'
            });
        }

        return res.status(500).json({
            error: 'No se pudo agregar el estudiante',
            detalle: error.message
        });
    }
});


// ===============================
// LEER TODOS LOS ESTUDIANTES
// GET /estudiantes
// ===============================
router.get('/', async (req, res) => {
    try {
        const [estudiantes] = await pool.execute(
            `SELECT
                e.*,
                c.nombre_curso,
                c.anio,
                c.division,
                c.turno,
                c.ciclo_lectivo
             FROM estudiantes e
             LEFT JOIN curso c
                ON e.id_curso = c.id_curso
             ORDER BY e.id_estudiante`
        );

        return res.status(200).json(estudiantes);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener los estudiantes',
            detalle: error.message
        });
    }
});


// ===============================
// LEER UN ESTUDIANTE POR ID
// GET /estudiantes/:id
// ===============================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [estudiantes] = await pool.execute(
            `SELECT
                e.*,
                c.nombre_curso,
                c.anio,
                c.division,
                c.turno,
                c.ciclo_lectivo
             FROM estudiantes e
             LEFT JOIN curso c
                ON e.id_curso = c.id_curso
             WHERE e.id_estudiante = ?`,
            [id]
        );

        if (estudiantes.length === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        return res.status(200).json(estudiantes[0]);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener el estudiante',
            detalle: error.message
        });
    }
});


// ===============================
// EDITAR UN ESTUDIANTE
// PUT /estudiantes/:id
// ===============================
router.put('/:id', async (req, res) => {
    const { id } = req.params;

    const {
        nombre,
        apellido,
        dni,
        fecha_nacimiento,
        nombre_tutor,
        telefono_tutor,
        email_tutor,
        id_curso
    } = req.body;

    if (id_curso === undefined || id_curso === null || id_curso === '') {
        return res.status(400).json({
            error: 'El curso es obligatorio'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE estudiantes
             SET nombre = ?,
                 apellido = ?,
                 dni = ?,
                 fecha_nacimiento = ?,
                 nombre_tutor = ?,
                 telefono_tutor = ?,
                 email_tutor = ?,
                 id_curso = ?
             WHERE id_estudiante = ?`,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                nombre_tutor,
                telefono_tutor,
                email_tutor,
                id_curso,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Estudiante actualizado correctamente'
        });

    } catch (error) {
        if (error.code === 'ER_NO_REFERENCED_ROW_2') {
            return res.status(400).json({
                error: 'El curso seleccionado no existe'
            });
        }

        return res.status(500).json({
            error: 'No se pudo actualizar el estudiante',
            detalle: error.message
        });
    }
});


// ===============================
// ELIMINAR UN ESTUDIANTE
// DELETE /estudiantes/:id
// ===============================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            `DELETE FROM estudiantes
             WHERE id_estudiante = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Estudiante eliminado correctamente'
        });

    } catch (error) {
        if (
            error.code === 'ER_ROW_IS_REFERENCED_2' ||
            error.code === 'ER_ROW_IS_REFERENCED'
        ) {
            return res.status(409).json({
                error: 'No se puede eliminar el estudiante porque tiene registros relacionados, por ejemplo, asistencias u observaciones.'
            });
        }

        return res.status(500).json({
            error: 'No se pudo eliminar el estudiante',
            detalle: error.message
        });
    }
});

module.exports = router;
