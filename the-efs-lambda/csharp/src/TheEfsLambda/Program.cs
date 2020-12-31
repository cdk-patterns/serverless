using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheEfsLambda
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheEfsLambdaStack(app, "TheEfsLambdaStack");
            app.Synth();
        }
    }
}
