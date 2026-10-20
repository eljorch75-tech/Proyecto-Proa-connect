
const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();


// ============================================
// AGREGAR UN DOCENTE
// POST /docentes
// ============================================
router.post('/', async (req, res) => {
    const {
        nombre,
        apellido,
        dni,
        email,
        telefono
    } = req.body;

    if (!nombre || !apellido || !dni) {
        return res.status(400).json({
            error: 'Nombre, apellido y DNI son obligatorios'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO docentes
            (nombre, apellido, dni, email, telefono)
            VALUES (?, ?, ?, ?, ?)`,
            [nombre, apellido, dni, email, telefono]
        );

        return res.status(201).json({
            mensaje: 'Docente agregado correctamente',
            id_docente: resultado.insertId
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo agregar el docente',
            detalle: error.message
        });
    }
});


// ============================================
// OBTENER TODOS LOS DOCENTES
// GET /docentes
// ============================================
router.get('/', async (req, res) => {
    try {
        const [docentes] = await pool.execute(
            `SELECT id_docente, nombre, apellido, dni, email, telefono
             FROM docentes
             ORDER BY apellido, nombre`
        );

        return res.status(200).json(docentes);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener los docentes',
            detalle: error.message
        });
    }
});


// ============================================
// OBTENER UN DOCENTE POR ID
// GET /docentes/:id
// ============================================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [docentes] = await pool.execute(
            `SELECT id_docente, nombre, apellido, dni, email, telefono
             FROM docentes
             WHERE id_docente = ?`,
            [id]
        );

        if (docentes.length === 0) {
            return res.status(404).json({
                error: 'Docente no encontrado'
            });
        }

        return res.status(200).json(docentes[0]);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener el docente',
            detalle: error.message
        });
    }
});


// ============================================
// ACTUALIZAR UN DOCENTE
// PUT /docentes/:id
// ============================================
router.put('/:id', async (req, res) => {
    const { id } = req.params;

    const {
        nombre,
        apellido,
        dni,
        email,
        telefono
    } = req.body;

    if (!nombre || !apellido || !dni) {
        return res.status(400).json({
            error: 'Nombre, apellido y DNI son obligatorios'
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE docentes
             SET nombre = ?,
                 apellido = ?,
                 dni = ?,
                 email = ?,
                 telefono = ?
             WHERE id_docente = ?`,
            [nombre, apellido, dni, email, telefono, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Docente no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Docente actualizado correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo actualizar el docente',
            detalle: error.message
        });
    }
});


// ============================================
// ELIMINAR UN DOCENTE
// DELETE /docentes/:id
// ============================================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            `DELETE FROM docentes
             WHERE id_docente = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Docente no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Docente eliminado correctamente'
        });

    } catch (error) {
        if (error.code === 'ER_ROW_IS_REFERENCED_2') {
            return res.status(409).json({
                error: 'No se puede eliminar el docente porque está relacionado con otros registros, como usuarios u observaciones.'
            });
        }

        return res.status(500).json({
            error: 'No se pudo eliminar el docente',
            detalle: error.message
        });
    }
});


module.exports = router;
