export {};

const express = require('express');

function apiRoutes(){
    const routes = new express.Router();

    routes.get('/add', (req:any, res:any) => {
        let firstNum = req?.query?.firstNum ?? 0;
        let secondNum = req?.query?.secondNum ?? 0;

        let result = Number(firstNum) + Number(secondNum);
        console.log(`result of ${firstNum} + ${secondNum} = ${result}`)

        res.status(200).json({"result":result})
    });

    routes.get('/subtract', (req:any, res:any) => {
        let firstNum = req?.query?.firstNum ?? 0;
        let secondNum = req?.query?.secondNum ?? 0;

        let result = Number(firstNum) - Number(secondNum);
        console.log(`result of ${firstNum} - ${secondNum} = ${result}`)

        res.status(200).json({"result":result})
    });

    routes.get('/multiply', (req:any, res:any) => {
        let firstNum = req?.query?.firstNum ?? 0;
        let secondNum = req?.query?.secondNum ?? 0;

        let result = Number(firstNum) * Number(secondNum);
        console.log(`result of ${firstNum} * ${secondNum} = ${result}`)

        res.status(200).json({"result":result})
    });

    return routes;
}


const app = express()
    .use(express.json())
    .use(apiRoutes());

const isInLambda = !!process.env.LAMBDA_TASK_ROOT;
if (isInLambda) {
    const serverlessExpress = require('aws-serverless-express');
    const server = serverlessExpress.createServer(app);
    exports.main = (event:any, context:any) => serverlessExpress.proxy(server, event, context)
} else {
    app.listen(3000, () => console.log(`Listening on 3000`));
}