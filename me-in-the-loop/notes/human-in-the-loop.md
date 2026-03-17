Working title: Me in the loop: my adventures designing software with AI

"The human messiness isn't a embarrassing qualifier to apologise for. It's the actual subject."

- processexecutor - mysqlinput. end of day writing wrong code (knew it was wrong, too tired). New day, relook at code, hey why can't I do xxx? Word the prompt better, get correct answer

- design patterns: artifactfactory, runnerfactory, visitor pattern (runners and operations)

- GREAT for code docs

- comical end-of-day antics. Me brain-dead, chat dropped to lower model, often giving code that used wrong variables or assumptions. Drunkenly persuing options we had long ago discarded, circling around the drain. 

- very elegant, very cool design. (I still don't think of it as "my" design.) StateDelta registry, whole statedelta system. The fact that artifacts run themselves. core of the system is (looks) simple.

- real design click was converting artifacts not to commands, but operations, which know how to convert themselves to commands. Could throw out the visitor pattern and separation of concerns (SOCs) were MUCH clearer. (Chat had to push the inversion. I was trying to make the CliCommand produce itself from an Operation (from_operation()), but that was assbackwards. MUCH better is Operation->to_cli_command()). Command->service() was very confusing. 

- I'm not very good at SOCs, but chat kept pushing it. (thank goodness).

- The ProcessExecutor is gold. It is the only class that executes commands. It can accept a file as input (stdin), captures stdout and stderr and returns everything in a CommandResult. Once it was refactored to accept a CliCommand (i/of cmd string), everything was possible: reading from stdin, passing envvars etc. 

- "Good engineers reduce the number of decisions other people must make."

- "2. The real hard problem in software. The real problem is: Making correct decisions in the right place." Very interesting discussion about old-fashioned OO "upbringing" vs what works now.

- Modern PHP. I love it!

- getting confused for the 100th time about docker and volumes and why can't I connect to the db??!

- mutation bug. Was partially having possibly mutable objects (make everything private readonly and add getters). But actually caused by (a) assigning source and target *refs* to the ArtifactEnv which probably (?) messed around with them and (b) using putenv() deep in  FileEnvReader (moral: don't use putenv in application code.)

- the docker-runners saga, lots of files and sweat to create dockerexec and dockerrun and dockermysql runners. But after circling around and around (problems with db-import finding the file) we decided to run purely in-container. Argh, why didn't "we" do that from the beginnning? Points to a deeper problem: the human can't prompt the ai to the "correct" solution if they don't know what it looks like. I didn't have enough knowledge of docker and its consequences. But I guess I learnt the hard way. 

- sometime later we figured out that I needed to create my OWN container, otherwise I didn't have access to the different dbs. Started it late one afternoon, and prob after a set of hallucinations and misunderstandings, abandoned it the next day. Two days later it turned out to be the solution that got rid of all the docker code, (prob) allows the same code to be in docker or on the webhost. Finally got rid of the volume/filesystem mapping problems that kept tripping me up. 

- (Spent a couple of days messing around with trying to write a cnf file for mysql but it was crossing envs and screwing up). Now mysql pw is passed in as env-var to CliCommand and so on to the ProcessExecutor.)

- won't save me from myself. Forgot that I had "solved" the mysql problem the previous day (need to pass password via proc_open() env-vars), and merrily started trying to solve problems I didn't have (trying to create my own container). So the human is still in control. And probably a good thing too?

- :-( The pretty visitor-pattern got tossed out. Instead of operation->run_with() we added operation->to_cli_command(). That simplified the design. Now no need for multiple HostRunner, just a single one that says run(operation->to_cli_command())

- "yeah, I could have figured that out". Induces a certain sort of laziness.

- talking of which: I LOVE copilot's ability to write code docs. Usually does a much better job than I could. I turn off copilot except for docs. I prefer to type it in myself and experience the pain of forgetting semis etc.  (Early on experience, chat would suggest a class, I would go to write it, and discover that I had already written it, but I didn't remember doing it.)

- config chasing. Several separate days spent dealing with config problems (docker, wp, mappings etc). Wildly frustrating. Scenario: spend a day chasing the problem, trying this, trying that, chat saying we're really close! end of the day I'm frustrated, tired and can't think (and of course chat has dropped down). Next day: I have to reassess the situation, understand the complexity, understand what the problem actually is, calmly and clearly explain to chat what we've tried, what worked and didn't, what my analysis is, and then we can usually solve it. (something very human-loopish about it).

- one long-running battle was getting docker apache to find the corect wordpress files. Bughunting extended over several sessions. Eliminated db prob, mysql access, etc probs. Underlying symptom is that wp plugins list and show theme were incorrect. Solution was to add entrypoint to dockerfile.wordpress. (And I upped to paid version of chatgpt afer it dropped down to super dumb mode in the middle of the hunt.) But I learned a lot more about running wpcli cmds in the (docker exec -it local_wp bash)

- I HATE config problems (it's a distraction from coding). Prob wouldn't have the stamina to fix them by myself. Or it would take a lot longer. 

- Personality change from free to plus (avail for free one-month trial). Less rah-rah you can do it! Less coachy. More business-like. Somewhat slower (longer thinking time). Answers not always qualitatively better. Can still get confused. 

- The bot is not your "friend"

- Weird horrible problem with getting wpcli and the websites to agree on a wp-config to use (non-standard wp setup). Docker mount problem.

- So many hours/days spent trying to get docker working correctly. Would have love to have done without, but when it works then testing is SO much easier (and safer). Massive amount of confusion caused by multi-envs (local etc), non-standard wp install, docker misunderstandings (I didn't realise vols needed rebuilding after changing, lead to endless adding and deleting of wp-config or not, ). when docker came crashing into wpcli, wp, websites and mig tool. Back-and-forth: search-replace works, websites don't and vv (endlessly!)

- debugging with ai. Not nec the magic bullet. Human needs to understand the problem, even if they can't see the solution (that's where ai is good), but if you keep feeding it irrelevant info it will keep cheerfully giving you solutions that don't help.

- chatgpt version. Started with free, 25/2 upgraded to one-month free plus. Anxiety at not using it enough, then realising that I can hire a design partner and hacker for 20 euros a month. I can't even get a (competent) junior programmer for that hourly amount. 

- speed up: functions like regex and url validation. Some bugs (esp config). 

- back and forth about design. "old-school" idea of reuse and class hierarchies. "new-school" duplication is not the enemy. Classes isolate decisions. May mean repetition, and that's still a prob to be solved (eg source and target db backups)

- why I typed (most of) the code myself. Personal quirk. I don't absorb information unless it passes through my fingers (writing or typing). It was essential to me that I understand the software that I'm writing. By typing it (and continually forgetting the bloody semi-c's) I feel that I know it better. Just reading code doesn't necessarily give enlightenment.  But I'll happily and unquestioningly accept stuff like regex or url validation. 

- The Design

- The relief when I stopped fighting with docker, and built a migration-container. Could throw out all the docker-specific stuff and the result HostRunner is clean and simple.

- First version was naive and embarrassing. It got the job done, but was brittle and messy. Naive php as I was fumbling around after python. 

- And sometimes there is just so much information it's overwhelming. A seemingly small question (what should validation look like for search-replace) produces a whole bunch of suggestions and advice (ugh, this is going to take a while to implement).

- lots and lots of refactors. But each time the cascade-effect was minimal. Worst is changing artifacts, but everything else is clean. g


run_migration.php
    ↓
MigrationScript
    ↓
Artifacts / Operations (pure, environment-agnostic)
    ↓
RunnerFactory (chosen at bootstrap)
        ↙                ↘
DockerRunnerFactory   DirectRunnerFactory
        ↓                     ↓
   Docker runners        Direct runners


CommandResult matrix
| **Scenario**       | **executed** | **exitcode** |
| ------------------ | ------------ | ------------ |
| Real success       | true         | 0            |
| Real failure       | true         | non-zero     |
| Dry-run simulation | false        | 0            |


Docker and wordpress

/wordpress → mounted to /var/www/html
Contains:
  index.php (router)
  wp/ (core)
  wp-config.php
  wp-config/
  wp-content/

Migration container:
- mounts project root → /antoniuskoor
- runs WP-CLI against that
- connects to all db containers  


Snippets of the wp-cli convo
line 30415
Second: your discomfort is a _signal_, not a problem

This line is the key one:

> _“The first lot of code is a real hack; I don't trust it.”_

That’s not guilt — that’s **professional judgement** kicking in.

There are only three sane responses when you reach that point:

1.  Stop and revert to manual ops forever
2.  Hand responsibility to a third-party tool
3.  **Refactor until you trust the code**

# Conversations with Claude
## AI can't save you from yourself

"That's a title.

Or at least the core of one. "AI can't save you from yourself" is punchy, honest, and cuts against the current hype grain without being a contrarian hot-take. It's earned, not performative.

And it's a theme that could run through the whole series as a quiet thread, not just one article. The Docker piece is the clearest example — you needed to rebuild your mental model and no amount of AI back-and-forth could do that for you. But it sounds like the class architecture wrestling had the same quality. You had an instinct, you pushed back, you had to understand *why* the answer was what it was before you could trust it.

That's actually a sophisticated and useful thing to say about working with AI that most current writing misses. The tools are good at a lot, but they can't see your blind spots. Only you can do that, and only once you know they're there.

It also reframes the human-in-the-loop concept more precisely. It's not just "human checks AI output for errors." It's "human is responsible for knowing what they don't know." Which is harder and more interesting.

That could be the spine of the whole series."

## the human messiness
"mm interesting thanks. Um, these are a couple of points from my notes (yes, I had already started them :-))
- the docker-runners saga, lots of files and sweat to create dockerexec and dockerrun and dockermysql runners. But after circling around and around (problems with db-import finding the file) we decided to run purely in-container. Argh, why didn't "we" do that from the beginnning? Points to a deeper problem: the human can't prompt the ai to the "correct" solution if they don't know what it looks like. I didn't have enough knowledge of docker and its consequences. But I guess I learn the hard way. 
- won't save me from myself. Forgot that I had "solved" the mysql problem the previous day (need to pass password via proc_open() env-vars), and merrily started trying to solve problems I didn't have (trying to create my own container). So the human is still in control. And probably a good thing too?
- config chasing. Several separate days spent dealing with config problems (docker, wp, mappings etc). Wildly frustrating. Scenario: spend a day chasing the problem, trying this, trying that, chat saying we're really close! end of the day I'm frustrated, tired and can't think (and of course (free) chat has dropped down). Next day: I have to reassess the situation, understand the complexity, understand what the problem actually is, calmly and clearly explain to chat what we've tried, what worked and didn't, what my analysis is, and then we can usually solve it. (something very human-loopish about it).
- debugging with ai. Not nec the magic bullet. Human needs to understand the problem, even if they can't see the solution (that's where ai is good), but if you keep feeding it irrelevant info it will keep giving you solutions that don't help."

"These are good. Really good. And they're specific, which is what will make the writing work.

A few observations:

The first and second points are actually the same insight from different angles. Point one: you can't prompt toward a solution you can't imagine. Point two: you forgot a solution you'd already found and went in circles. Both are about the limits of what you bring to the collaboration, not the limits of AI. That's rich.

The config-chasing point is the most human and relatable, and buried in it is something really sharp — the *overnight reset*. Frustration, context loss, then calm reassessment the next morning produces the breakthrough. That's not an AI story, that's a thinking story. The AI is almost incidental to it. Worth drawing that out explicitly.

The debugging point is practically useful and quotable: "if you keep feeding it irrelevant information it will keep giving you solutions that don't help." That's a precise description of a failure mode people will immediately recognise.

One thing connecting all four: **the quality of the human's input determines the quality of the output**, but the human can only give good input from a position of sufficient understanding. **Which means there's a bootstrapping problem at the heart of AI-assisted learning. You have to know enough to ask well, but you're using AI partly because you don't know enough yet.**

That's the deeper problem your first point is pointing at. Did you find ways to break that loop, or did it just require the hard way every time?"

"I don't thI don't think I did, and I'm not sure what the solution is. But what often helps is that AI is good at offering a range of options. I've noticed (not just with this tool) that it often gives you something that you definitely wouldn't have thought of, but is a really good viable option. So maybe the human needs to remember to ask for options?"

"That's an honest answer, and probably the right one. There isn't a clean solution to the bootstrapping problem — and pretending there is would weaken the writing.

But what you've landed on is interesting: "ask for options" as a partial mitigation. It's a way of using AI's breadth to compensate for your own blind spots. You don't need to know the right question if you ask a wide enough one.

That's a concrete, actionable observation that readers can actually use. And it's earned — you found it through pain, not theory.

There's also something honest and valuable in saying "I don't know the full solution." A lot of AI writing is falsely tidy. Here's the problem, here's the fix, here's the lesson. Your experience is messier than that — sometimes you just learned the hard way, and the best you can do is know that going in. That's more useful to a reader than false resolution.

So maybe that section of the article doesn't end with an answer. It ends with "ask for options" as a partial tool, and an acknowledgement that some knowledge you just have to acquire the hard way before the collaboration can work properly. That's not a weakness in the writing — it's intellectual honesty, and it'll read as trustworthy.

You're accumulating quite a lot of material now. Have you thought about whether this is one article that covers the full experience, or whether the Docker/AI-limits thread is its own separate piece from the architecture one?"