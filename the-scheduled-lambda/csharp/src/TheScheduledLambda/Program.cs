using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheScheduledLambda
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheScheduledLambdaStack(app, "TheScheduledLambdaStack");
            app.Synth();
        }
    }
}
