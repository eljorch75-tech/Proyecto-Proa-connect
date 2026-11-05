const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();

// =====================================
// AGREGAR ESTUDIANTE
// POST /api/estudiantes
// =====================================
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

    if (!id_curso) {
        return res.status(400).json({
            error: 'Tenés que seleccionar un curso'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO estudiantes
            (nombre, apellido, dni, fecha_nacimiento,
             nombre_tutor, telefono_tutor, email_tutor, id_curso)
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

        res.status(201).json({
            mensaje: 'Estudiante agregado correctamente',
            id: resultado.insertId
        });

    } catch (error) {
        console.error('ERROR AL AGREGAR ESTUDIANTE:', error);

        res.status(500).json({
            error: 'No se pudo agregar el estudiante',
            detalle: error.message
        });
    }
});


// =====================================
// LISTAR TODOS LOS ESTUDIANTES
// GET /api/estudiantes
// =====================================
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
             ORDER BY e.id_estudiante DESC`
        );

        res.json(estudiantes);

    } catch (error) {
        console.error('ERROR AL LISTAR ESTUDIANTES:', error);

        res.status(500).json({
            error: 'No se pudieron obtener los estudiantes',
            detalle: error.message
        });
    }
});


// =====================================
// BUSCAR ESTUDIANTE POR ID
// GET /api/estudiantes/:id
// =====================================
router.get('/:id', async (req, res) => {
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
            [req.params.id]
        );

        if (estudiantes.length === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        res.json(estudiantes[0]);

    } catch (error) {
        console.error('ERROR AL BUSCAR ESTUDIANTE:', error);

        res.status(500).json({
            error: 'No se pudo obtener el estudiante',
            detalle: error.message
        });
    }
});


// =====================================
// EDITAR ESTUDIANTE
// PUT /api/estudiantes/:id
// =====================================
router.put('/:id', async (req, res) => {
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

    if (!id_curso) {
        return res.status(400).json({
            error: 'Tenés que seleccionar un curso'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE estudiantes SET
                nombre = ?,
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
                req.params.id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        res.json({
            mensaje: 'Estudiante actualizado correctamente'
        });

    } catch (error) {
        console.error('ERROR AL EDITAR ESTUDIANTE:', error);

        res.status(500).json({
            error: 'No se pudo actualizar el estudiante',
            detalle: error.message
        });
    }
});


// =====================================
// ELIMINAR ESTUDIANTE
// DELETE /api/estudiantes/:id
// =====================================
router.delete('/:id', async (req, res) => {
    try {
        const [resultado] = await pool.execute(
            `DELETE FROM estudiantes
             WHERE id_estudiante = ?`,
            [req.params.id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Estudiante no encontrado'
            });
        }

        res.json({
            mensaje: 'Estudiante eliminado correctamente'
        });

    } catch (error) {
        console.error('ERROR AL ELIMINAR ESTUDIANTE:', error);

        res.status(500).json({
            error: 'No se pudo eliminar el estudiante',
            detalle: error.message
        });
    }
});

module.exports = router;