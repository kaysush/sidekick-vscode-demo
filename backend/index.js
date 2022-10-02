const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

const app = express()
app.use(cors())


const port = process.env.PORT

// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/health', (req, res) => {
    res.send("This is the health endpoint.")
})

app.post("/calculate", (req, res) => {
    const request = req.body
    const x = Number(request.x)
    const y = Number(request.y)
    const operator = request.op

    switch(operator) {
        case '+': 
            var result = x + y;
            res.send(JSON.stringify({result : result}))
            break;
        case '-':
            var result = x - y;
            res.send(JSON.stringify({result : result}))
            break;
        case '*':
            var result = x * y;
            res.send(JSON.stringify({result : result}))
            break;
        case '/':
            var result = x / y;
            res.send(JSON.stringify({result : result}))
            break;
        default:
            res.status(500).send(`Operator ${operator} not supported.`);
    }
})

app.listen(port, () => console.log(`Backend started on port ${port}!`));