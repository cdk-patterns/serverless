export {};

const express = require('express');

/**
 * All of our routes are defined inside this lambda and orchestrated using express.js
 */
function apiRoutes(){
    const routes = new express.Router();

    routes.get('/add', (req:any, res:any) => {
        // pull firstNum and secondNum from queryparams, default to 0
        let firstNum = req?.query?.firstNum ?? 0;
        let secondNum = req?.query?.secondNum ?? 0;

        let result = Number(firstNum) + Number(secondNum);
        console.log(`result of ${firstNum} + ${secondNum} = ${result}`)

        res.status(200).json({"result":result})
    });

    routes.get('/subtract', (req:any, res:any) => {
        // pull firstNum and secondNum from queryparams, default to 0
        let firstNum = req?.query?.firstNum ?? 0;
        let secondNum = req?.query?.secondNum ?? 0;

        let result = Number(firstNum) - Number(secondNum);
        console.log(`result of ${firstNum} - ${secondNum} = ${result}`)

        res.status(200).json({"result":result})
    });

    routes.get('/multiply', (req:any, res:any) => {
        // pull firstNum and secondNum from queryparams, default to 0
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

/**
 * Since this is a monolith, we can start it locally to do development
 */
const isInLambda = !!process.env.LAMBDA_TASK_ROOT;
if (isInLambda) {
    const serverlessExpress = require('aws-serverless-express');
    const server = serverlessExpress.createServer(app);
    exports.main = (event:any, context:any) => serverlessExpress.proxy(server, event, context)
} else {
    app.listen(3000, () => console.log(`Listening on 3000`));
}