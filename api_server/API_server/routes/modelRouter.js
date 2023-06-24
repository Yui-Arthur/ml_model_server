const modelController = require('../controllers/modelController')

const router = require('express').Router()
// const isAuthenticated = require('../policies/isAuthenticated')

// router.post('/addSensor', ModelController.addSensor)
router.get('/:modelName/check' , modelController.checkModel)
router.get('/:modelName/create/:maxToken', modelController.createModel)
router.get('/:modelName/delete', modelController.deleteModel)
router.post('/:modelName/:user' , modelController.getModel)
// router.get('/:id', ModelController.getOneSensor)
// router.put('/:id', isAuthenticated, sensorController.updateSensor)
// router.delete('/:id', isAuthenticated, sensorController.deleteSensor)

module.exports = router