```js
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
        email_tutor
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO estudiantes
            (nombre, apellido, dni, fecha_nacimiento, nombre_tutor, telefono_tutor, email_tutor)
            VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                nombre_tutor,
                telefono_tutor,
                email_tutor
            ]
        );

        return res.status(201).json({
            mensaje: 'Estudiante agregado correctamente',
            id: resultado.insertId
        });

    } catch (error) {
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
            `SELECT * FROM estudiantes`
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
            `SELECT * FROM estudiantes WHERE id = ?`,
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
        email_tutor
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE estudiantes
             SET nombre = ?,
                 apellido = ?,
                 dni = ?,
                 fecha_nacimiento = ?,
                 nombre_tutor = ?,
                 telefono_tutor = ?,
                 email_tutor = ?
             WHERE id = ?`,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                nombre_tutor,
                telefono_tutor,
                email_tutor,
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
            `DELETE FROM estudiantes WHERE id = ?`,
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
        return res.status(500).json({
            error: 'No se pudo eliminar el estudiante',
            detalle: error.message
        });
    }
});


module.exports = router;
```
