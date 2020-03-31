export {};

const express = require('express');

function apiRoutes(){
    const routes = new express.Router();

    routes.get('/v1/version', (req:any, res:any) => res.send({version: '1'}));

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