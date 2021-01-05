using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheLambdaPowerTuner
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheLambdaPowerTunerStack(app, "TheLambdaPowerTunerStack");
            app.Synth();
        }
    }
}
