```javascript
const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();


// ===============================
// AGREGAR UNA ASISTENCIA
// POST /asistencias
// ===============================
router.post('/', async (req, res) => {

    const {
        curso,
        fecha,
        estado,
        motivo_justificacion,
        id_estudiante
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `INSERT INTO asistencias
            (curso, fecha, estado, motivo_justificacion, id_estudiante)
            VALUES (?, ?, ?, ?, ?)`,
            [
                curso,
                fecha,
                estado,
                motivo_justificacion,
                id_estudiante
            ]
        );

        return res.status(201).json({
            mensaje: 'Asistencia agregada correctamente',
            id: resultado.insertId
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo agregar la asistencia',
            detalle: error.message
        });

    }
});


// ===============================
// LEER TODAS LAS ASISTENCIAS
// GET /asistencias
// ===============================
router.get('/', async (req, res) => {

    try {

        const [asistencias] = await pool.execute(
            `SELECT * FROM asistencias`
        );

        return res.status(200).json(asistencias);

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudieron obtener las asistencias',
            detalle: error.message
        });

    }
});


// ===============================
// LEER UNA ASISTENCIA POR ID
// GET /asistencias/:id
// ===============================
router.get('/:id', async (req, res) => {

    const { id } = req.params;

    try {

        const [asistencias] = await pool.execute(
            `SELECT * FROM asistencias
             WHERE id_asistencia = ?`,
            [id]
        );

        if (asistencias.length === 0) {

            return res.status(404).json({
                error: 'Asistencia no encontrada'
            });

        }

        return res.status(200).json(asistencias[0]);

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo obtener la asistencia',
            detalle: error.message
        });

    }
});


// ===============================
// EDITAR UNA ASISTENCIA
// PUT /asistencias/:id
// ===============================
router.put('/:id', async (req, res) => {

    const { id } = req.params;

    const {
        curso,
        fecha,
        estado,
        motivo_justificacion,
        id_estudiante
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `UPDATE asistencias
             SET curso = ?,
                 fecha = ?,
                 estado = ?,
                 motivo_justificacion = ?,
                 id_estudiante = ?
             WHERE id_asistencia = ?`,
            [
                curso,
                fecha,
                estado,
                motivo_justificacion,
                id_estudiante,
                id
            ]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: 'Asistencia no encontrada'
            });

        }

        return res.status(200).json({
            mensaje: 'Asistencia actualizada correctamente'
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo actualizar la asistencia',
            detalle: error.message
        });

    }
});


// ===============================
// ELIMINAR UNA ASISTENCIA
// DELETE /asistencias/:id
// ===============================
router.delete('/:id', async (req, res) => {

    const { id } = req.params;

    try {

        const [resultado] = await pool.execute(
            `DELETE FROM asistencias
             WHERE id_asistencia = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: 'Asistencia no encontrada'
            });

        }

        return res.status(200).json({
            mensaje: 'Asistencia eliminada correctamente'
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo eliminar la asistencia',
            detalle: error.message
        });

    }
});


module.exports = router;
```
