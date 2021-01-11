using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheStateMachine
{
    sealed class Program
    {

        public static void Main(string[] args)
        {
            var app = new App();
            new TheStateMachineStack(app, "TheStateMachineStack");
            app.Synth();
        }
    }
}
