const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();

// ===================================
// LISTAR TODOS LOS CURSOS
// GET /api/cursos
// ===================================
router.get('/', async (req, res) => {
    try {
        const [cursos] = await pool.execute(
            `SELECT
                id_curso,
                nombre_curso,
                anio,
                division,
                turno,
                ciclo_lectivo
             FROM curso
             ORDER BY anio, division`
        );

        res.status(200).json(cursos);

    } catch (error) {
        console.error('Error al listar cursos:', error);

        res.status(500).json({
            error: 'No se pudieron listar los cursos',
            detalle: error.message
        });
    }
});

module.exports = router;