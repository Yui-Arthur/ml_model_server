const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

require('dotenv').config()

const app = express()
app.use(bodyParser.json())
// app.use(express.static('view/dist'))


const corsOptions ={
    origin:['http://localhost:8088'], 
    credentials:true,            //access-control-allow-credentials:true
    optionSuccessStatus:200
}
app.use(cors(corsOptions));

// require('./passport')

//routers
const modelRouter = require('./routes/modelRouter')

const url = '/api/'

app.use(url+'llm', modelRouter)


app.listen(process.env.PORT || 8088, function(req , res ){
    console.log('server is running...'); 
    // console.log(process.env.PORT);
})