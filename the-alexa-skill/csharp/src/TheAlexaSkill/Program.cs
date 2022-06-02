using Amazon.CDK;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TheAlexaSkill
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            new TheAlexaSkillStack(app, "TheAlexaSkillStack");
            app.Synth();
        }
    }
}
