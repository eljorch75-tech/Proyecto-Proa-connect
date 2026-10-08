const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();


// ===============================
// AGREGAR UNA OBSERVACIÓN
// POST /observaciones
// ===============================
router.post('/', async (req, res) => {

    const {
        fecha,
        tipo,
        descripcion,
        requiere_seguimiento,
        id_estudiante,
        id_docente
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `INSERT INTO observaciones
            (fecha, tipo, descripcion, requiere_seguimiento, id_estudiante, id_docente)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                fecha,
                tipo,
                descripcion,
                requiere_seguimiento,
                id_estudiante,
                id_docente
            ]
        );

        return res.status(201).json({
            mensaje: 'Observación agregada correctamente',
            id: resultado.insertId
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo agregar la observación',
            detalle: error.message
        });

    }
});


// ===============================
// LEER TODAS LAS OBSERVACIONES
// GET /observaciones
// ===============================
router.get('/', async (req, res) => {

    try {

        const [observaciones] = await pool.execute(
            `SELECT * FROM observaciones`
        );

        return res.status(200).json(observaciones);

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudieron obtener las observaciones',
            detalle: error.message
        });

    }
});


// ===============================
// LEER UNA OBSERVACIÓN POR ID
// GET /observaciones/:id
// ===============================
router.get('/:id', async (req, res) => {

    const { id } = req.params;

    try {

        const [observaciones] = await pool.execute(
            `SELECT * FROM observaciones
             WHERE id_observacion = ?`,
            [id]
        );

        if (observaciones.length === 0) {

            return res.status(404).json({
                error: 'Observación no encontrada'
            });

        }

        return res.status(200).json(observaciones[0]);

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo obtener la observación',
            detalle: error.message
        });

    }
});


// ===============================
// EDITAR UNA OBSERVACIÓN
// PUT /observaciones/:id
// ===============================
router.put('/:id', async (req, res) => {

    const { id } = req.params;

    const {
        fecha,
        tipo,
        descripcion,
        requiere_seguimiento,
        id_estudiante,
        id_docente
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `UPDATE observaciones
             SET fecha = ?,
                 tipo = ?,
                 descripcion = ?,
                 requiere_seguimiento = ?,
                 id_estudiante = ?,
                 id_docente = ?
             WHERE id_observacion = ?`,
            [
                fecha,
                tipo,
                descripcion,
                requiere_seguimiento,
                id_estudiante,
                id_docente,
                id
            ]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: 'Observación no encontrada'
            });

        }

        return res.status(200).json({
            mensaje: 'Observación actualizada correctamente'
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo actualizar la observación',
            detalle: error.message
        });

    }
});


// ===============================
// ELIMINAR UNA OBSERVACIÓN
// DELETE /observaciones/:id
// ===============================
router.delete('/:id', async (req, res) => {

    const { id } = req.params;

    try {

        const [resultado] = await pool.execute(
            `DELETE FROM observaciones
             WHERE id_observacion = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: 'Observación no encontrada'
            });

        }

        return res.status(200).json({
            mensaje: 'Observación eliminada correctamente'
        });

    } catch (error) {

        return res.status(500).json({
            error: 'No se pudo eliminar la observación',
            detalle: error.message
        });

    }
});


module.exports = router;
