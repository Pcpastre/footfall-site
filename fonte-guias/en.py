BODY = {}

BODY["comecar"] = """
<p>You play Footfall by actually walking. The map is your city, through GPS, and you only move forward when you walk. This guide takes you from the first tap to your first session on the street.</p>

<h2>Account</h2>
<p>The game needs an account with an email and password: it keeps your character, your base and your progress in the cloud. On the start screen, tap <kbd>LOG IN / CREATE ACCOUNT</kbd>. The password has at least 8 characters, and sign-up is confirmed with a 6-digit code sent by email.</p>

<h2>Your survivor</h2>
<ol class="steps">
<li><b>Before you set off walking:</b> read the safety warnings and tap <kbd>GOT IT, LET'S GO</kbd>.</li>
<li><b>Appearance:</b> face, hair, skin and clothes.</li>
<li><b>Profession and traits:</b> each profession gives skills and a pool of points. Positive traits spend points; negative ones give them back.</li>
</ol>
<p>A few professions to start with:</p>
<ul>
<li><b>Unemployed:</b> no bonus, but the largest pool of points for traits.</li>
<li><b>Police officer</b> and <b>Military veteran:</b> better with firearms (the veteran already comes desensitized to panic).</li>
<li><b>Nurse</b> and <b>Doctor:</b> treat wounds faster and with fewer failures.</li>
<li><b>Carpenter:</b> builds and repairs the base better.</li>
<li><b>Delivery driver:</b> starts with the neighborhood already revealed on the map, and distance walked counts for more.</li>
<li><b>Burglar:</b> rummages 1.5× faster and makes less noise.</li>
</ul>
<p>Useful traits: <b>Light-footed</b> (less noise), <b>Eagle eyes</b> (sees farther), <b>Organized</b> (bigger backpack), <b>Thick skin</b> (fewer blows turn into wounds). Be careful with <b>Homebody</b> (gets tired far from the base) and <b>Smoker</b> (needs cigarettes).</p>
<p>You start with the basic kit in your backpack: bat, revolver with bullets, bandages, water, food, jeans and a school backpack.</p>
<div class="tip warn"><b>Death is permanent</b>If your character dies, they and their skills are gone. The base, the chests and the radio vault stay for the next one.</div>

<h2>The first night</h2>
<p>Before the map, the game offers <b>The last delivery</b>: you are a mail carrier on a stormy night, and it teaches you to crouch-walk, rummage, strike, shove and shoot. You can skip it with <kbd>GO STRAIGHT TO THE CITY</kbd> and play it later from the shelf of memories.</p>

<h2>Session</h2>
<p>On the map, tap <kbd>START SESSION</kbd> on the bottom bar. From then on your character walks with you. To stop, open the <kbd>⋯</kbd> menu:</p>
<ul>
<li><kbd>Sleep (end here)</kbd> at the base, at an outpost or in a tent: the character rests and recovers fatigue and health.</li>
<li><kbd>End session</kbd> anywhere else: you lose nothing, but the rest is poor.</li>
</ul>

<h2>Seeing and being seen</h2>
<ul>
<li>You see in a 110° cone in front of you, up to 120 m by day and 40 m at night. Buildings block your view.</li>
<li>The cone follows the top of your phone (compass). If the compass gets in the way, turn it off in Settings and use the stick to look around.</li>
<li>Zombies see you from about 15 m by day and 8 m at night, but a lit flashlight gets you seen from 30 m.</li>
<li>Walking makes little noise; running makes much more. Noise draws whoever is nearby.</li>
</ul>

<h2>The more you walk, the better the loot</h2>
<p>Distance walked in a session raises the chance of finding rare items (up to 15%). It only counts on foot: above about 25 km/h for a few seconds the game takes it as a vehicle, the distance stops counting and noise goes to the maximum.</p>

<div class="tip"><b>Crossing the street</b>On avenues, zombies stop and no fight starts: "Cross carefully" appears. Look at the real street, not the screen. Never play while driving.</div>
"""

BODY["saque"] = """
<p>The supermarkets, pharmacies, police stations, gas stations, schools, shops and houses of your neighborhood are in the game. Each kind of place has its own finds and its own dangers.</p>

<h2>Through the door or going in</h2>
<p>Once you are within 35 m of a place (houses: right up against them), tap <kbd>Loot</kbd>. You choose:</p>
<ul>
<li><b>Through the door:</b> fast, only the furniture by the entrance, and no rare items.</li>
<li><b>Enter:</b> opens the action screen inside the building. More furniture, more chance of rares, and more zombies. Buildings can have floors (<kbd>GO UP</kbd> / <kbd>GO DOWN</kbd>).</li>
</ul>
<p>If you move more than 20 m away in the middle of looting, it is interrupted.</p>

<h2>Furniture and noise</h2>
<p>Each piece of furniture has a time to rummage and a noise level: <b>silent</b>, <b>moderate noise</b> or <b>loud noise</b>. A drawer takes 1 s; a cash register, 2.5 s and makes noise; a locked armory, 5 s and a lot of noise. Stay still while you rummage and tap <kbd>Take all</kbd> at the end.</p>
<ul>
<li>Sometimes the furniture is empty.</li>
<li>Rummaging through glass and tin can cut your hand (shard).</li>
<li>Locked doors open with a crowbar (3 s, with noise) or when a zombie inside breaks the door down.</li>
</ul>

<h2>Restocked every week</h2>
<p>A looted place stays marked as "already looted" for 7 days; then it fills up again. The stock is the same for everyone: if "Another survivor took it first" appears, someone got there before you.</p>

<h2>Bodies</h2>
<p>Downed zombies stay on the ground for 2 hours. Each fight becomes a pile of bodies: <kbd>Search all</kbd> goes through all of them at once. Bodies carry things from their pockets, cloth and, sometimes, stamps. Uniformed zombies (police, firefighter, doctor…) carry what they used in life, and sometimes the whole uniform.</p>

<h2>Backpack and weight</h2>
<p>How much you carry is the sum of your clothing pockets and your backpack:</p>
<ul>
<li>Body pockets: 4 kg, plus the pockets of pants, vests, fanny pack and thigh pouch.</li>
<li>Backpacks: school 6 kg, gym bag 5, daypack 10, tactical 12, expedition pack 16.</li>
<li>Strength, Organized and Disorganized change that limit.</li>
</ul>
<p>Above the limit, <b>Heavy load</b> appears: you are slower in combat and noisier on the map.</p>
<p>The belt has 2 slots for what you need in hand fast (a 3rd with a tactical vest or tactical backpack). Long weapons go on your back.</p>
<div class="tip"><b>Tip</b>Medicine, ammo, throwables and batteries go to your pockets first. In combat, pulling anything else from the bottom of the backpack takes 2.5 s.</div>

<h2>Military bunkers</h2>
<p>Every month, some squares become bunkers with 3 to 6 floors going down, each darker and more dangerous, and each with better loot. Every floor starts in a safe room, where zombies cannot enter. A floor's generator turns on the light with 1 biodiesel. The vault door at the far end opens with the access card, or with a crowbar in 60 s and a lot of noise. The bunker restocks the following month.</p>
"""

BODY["combate"] = """
<p>When a zombie that is after you gets within 25 m, the game asks you to stop somewhere safe and opens the <b>action screen</b>: a pixel art scene of the place where you are, with the real streets, cars and buildings. You can also open it with the big <kbd>Action screen</kbd> button on the map.</p>
<p>Zombies within 120 m join the fight, a few at a time. At the base in safety, or while crossing an avenue, no fight starts.</p>

<h2>The three control schemes</h2>
<p>Choose in Settings → <kbd>CONTROLS</kbd> (or by tapping the status card during a fight):</p>
<ul>
<li><b>Simple</b> (default): one stick to walk and the <kbd>FIGHT</kbd> button. With it on, you face the nearest zombie; tap the right half of the screen to strike or shoot and the left half to shove. Running turns it off.</li>
<li><b>Two sticks:</b> the right one aims; tapping the screen strikes and shoves.</li>
<li><b>Automatic:</b> only the walking stick; strikes, shots and shoves happen on their own.</li>
</ul>

<h2>Shove</h2>
<p>The shove is your best defense: it knocks down or staggers, frees you from whoever grabbed you and lowers panic. It costs stamina and has a short wait between one and the next.</p>

<h2>Aiming and hitting</h2>
<ul>
<li>Choose the <kbd>TARGET</kbd>: head, body or legs.</li>
<li>On the head, a strike does more damage, but it can slip to the shoulder (less with more skill). A headshot does 2.5× damage.</li>
<li>Destroyed legs make the zombie crawl.</li>
<li>Hits with the tip of the weapon can be critical.</li>
</ul>

<h2>Stamina</h2>
<p>Running burns stamina fast; standing still brings it back. With little stamina, your strikes lose force. Fatigue, fever, cold, heat and pain lower your maximum stamina.</p>

<h2>Crouch</h2>
<p><kbd>CROUCH</kbd> makes you slow and unable to run, but distracted zombies take twice as long to notice you and need to be much closer. From behind, out of their sight, you can take them down silently.</p>

<h2>Weapons</h2>
<ul>
<li><b>Melee</b> (knife, bat, machete, axe, sledgehammer, katana…): wear down with every strike that lands, and break. You can repair them at the workbench or with tape and nails.</li>
<li><b>Firearms</b> (pistol, revolver, shotgun, .22 rifle, hunting rifle, submachine gun, assault rifle): don't wear down, but every shot draws zombies within 150 m. The silencer muffles a few pistol shots.</li>
<li><b>Bow and crossbow:</b> almost silent; some of the arrows come back after the fight.</li>
<li><b>Throwables:</b> bottle, rock, alarm clock and firework distract; the molotov sets the ground on fire.</li>
</ul>
<p>Reloading with ammo in your pocket is fast; if it is only in the backpack, it takes twice as long.</p>

<h2>Different zombies</h2>
<p>Besides the common one, there are uniformed zombies: the <b>inmate</b> is fast, the <b>soldier</b> and the <b>firefighter</b> take a lot of punishment (the firefighter doesn't catch fire), the <b>police officer</b> wears a vest, the <b>backpacker</b> carries more things. The <b>Brute</b> is huge, slow and takes six times more.</p>

<h2>Leaving the fight</h2>
<ul>
<li>The door icon (<kbd>Exit</kbd>) appears when no one is within 10 m and no one is after you.</li>
<li>Stay 40 m from everyone who saw you for a few seconds and they lose you.</li>
<li>Or run to the red edge of the scene.</li>
</ul>
<div class="tip"><b>Other survivors</b>Anyone near you in the real world shows up in the same scene, and the map warns you when someone is fighting close by.</div>
"""

BODY["saude"] = """
<p>Your survivor's body works like a body. Every zombie blow can become a wound on a part of the body, and every wound has its own treatment. It is all in <b>Character → Health</b>.</p>

<h2>Wounds</h2>
<ul>
<li><b>Scratch:</b> bleeds a little, closes in 1 day.</li>
<li><b>Laceration:</b> bleeds more, 3 days. Sometimes it becomes a <b>hemorrhage</b>, which bleeds very fast.</li>
<li><b>Bite:</b> bleeds and almost always gets infected.</li>
<li><b>Deep cut:</b> needs sutures.</li>
<li><b>Shard:</b> from glass while rummaging; remove it with tweezers.</li>
<li><b>Fracture:</b> needs a splint, 7 days.</li>
<li><b>Burn:</b> ointment and a wrap.</li>
</ul>

<h2>Treating step by step</h2>
<ol class="steps">
<li><b>Tourniquet</b> (hemorrhage): stop the blood with a tourniquet or cloth. Don't leave it more than 2 hours without suturing.</li>
<li><b>Clean and disinfect:</b> saline, alcohol or cachaça.</li>
<li><b>Remove the shard</b> with tweezers, when there is one.</li>
<li><b>Suture</b> with a suture kit (deep cuts and hemorrhages).</li>
<li><b>Bandage:</b> dressing, gauze, bandage or cloth.</li>
</ol>
<p>The wound only heals with every step done. Dressings get dirty after 12 hours (24 with medical tape) and need changing; cloth already counts as dirty. A dirty wound gets infected, and an ordinary infection is cured with antibiotics.</p>

<h2>The zombie infection</h2>
<div class="tip warn"><b>There is no cure</b>A bite almost always infects; a laceration or scratch, sometimes. The infection runs in real time: a few days with nothing, then fever, then delirium, and in 7 days the character dies.</div>

<h2>Hunger and thirst</h2>
<p>Your character uses up food and water like a person, and more when walking. The warnings come in three levels ("Hungry", "Starving", "Sick with hunger"). Only at the last level does the character lose health, and only during a session: with the app closed, no one starves to death.</p>
<p>Cooked food goes further and lasts longer. To cook, light a campfire or the wood stove (lighter and plank). Rainwater can make you sick: boil it first.</p>

<h2>Cold and heat</h2>
<p>The temperature is your city's, right now. In the rain without a raincoat, and at night, it is colder; below 16 °C you need warm clothes. In the heat, heavy clothing tires you and a cap helps. Cold burns food; heat burns water.</p>

<h2>Fatigue and sleep</h2>
<p>Walking, running and fighting tire you. Ending the session with <kbd>Sleep</kbd> at the base, at an outpost or in a tent recovers fatigue and health while you are away. With a bed at the base, the rest is much better; away from it, a sleeping bag helps.</p>

<h2>The mind too</h2>
<p>Panic in a fight takes away accuracy; shoving relieves it. Staying still at the base for too long makes the character bored, and going through a lot of bad things makes them sad. Going out for a walk helps.</p>

<h2>Clothes</h2>
<p>Clothes protect the part of the body they cover. Torn clothes protect half as much: sew them with a needle, thread and a cloth.</p>

<h2>When they die</h2>
<p>The character and their skills are gone. Everything they carried stays in a pile where they fell: for 24 hours only you can see it, then anyone can, and a zombie with their face stands guard. The wallet loses 15% of its stamps. The base, the chests, the radio vault and the clothes in the wardrobe stay. Tap <kbd>New survivor</kbd> and get back on the street.</p>
"""

BODY["base"] = """
<p>The base is where you keep what you've gathered, sleep and cook. Every night the dead pound on the walls.</p>

<h2>Marking out</h2>
<ol class="steps">
<li>With the session on, open the base menu and tap <kbd>Mark out base</kbd>.</li>
<li>Tap the grid to mark the corners (up to 60 m from you). Tap the first corner again to close it.</li>
<li>Tap <kbd>Mark out base</kbd> to confirm.</li>
</ol>
<p>It starts at 50 m², and grows with expansion kits and with people in the group. It must be at least 30 m from another base.</p>
<div class="tip warn"><b>Privacy</b>The base is visible to anyone passing nearby. Don't mark out your base where you live. At home, use an outpost.</div>

<h2>Walls, doors and windows</h2>
<ul>
<li>Building walls are free and don't fall.</li>
<li>Your own walls: 1 plank and 1 nail every 4 m. You can reinforce them with sheet metal and then with concrete.</li>
<li>Door: 3 planks and 2 nails. Window: 2 planks and 1 nail (nailed planks reinforce it).</li>
<li><kbd>Repair the weakest wall</kbd> uses 1 plank and 1 nail.</li>
</ul>
<p>An open door or a fallen wall = an open base.</p>

<h2>Furniture</h2>
<p>On the action screen, inside the base, use the hammer to build and <kbd>USE</kbd> to use:</p>
<ul>
<li><b>Chest:</b> 40 kg each. Nothing goes in by itself: you store it.</li>
<li><b>Workbench:</b> recipes and repairs.</li>
<li><b>Bed:</b> much better rest. <b>Stretcher:</b> treated wounds heal faster.</li>
<li><b>Table</b>, <b>campfire</b> (light and noise at night), <b>wood stove</b> (almost no light).</li>
<li><b>Rain barrel:</b> collects water when it really rains.</li>
<li><b>Watchtower:</b> see farther near the base. <b>Floodlight:</b> needs a generator and gasoline.</li>
<li><b>Mailbox:</b> the market (see the group guide).</li>
</ul>

<h2>Garden</h2>
<p>Up to 4 garden beds: <kbd>Plant</kbd> the seeds, <kbd>Water</kbd> them (each watering lasts a day) and <kbd>Harvest</kbd> after about 3 watered days.</p>

<h2>Traps</h2>
<ul>
<li><b>Stakes</b> and <b>covered pit:</b> catch attackers and need to be reset.</li>
<li><b>Tin can wire:</b> an alarm that warns you and reduces the damage.</li>
</ul>

<h2>The nightly attack</h2>
<p>At 1 AM the base is attacked, even with the app closed (up to 3 missed nights are resolved when you come back). Bigger walls, a lit campfire and a floodlight that is on draw more of them. The traps catch some; the rest pound on the walls, doors and windows.</p>
<p>If a wall falls or a door is left open, the chests lose part of what is inside (clothes stay). The week's horde also passes through the base if its route comes close.</p>
<div class="tip"><b>Being there helps</b>If you are at the base with the session on, the damage is cut in half.</div>

<h2>The radio vault and the outposts</h2>
<p>The radio vault is yours alone, with 300 kg, and you reach it from any outpost or tent. In it are the vault, the workbench, the radio to go back to the base, the mail (market and general store), the wardrobe and the shelf of memories. The clothes in the wardrobe stay even after death.</p>
<p>You can have up to 10 outposts, between 200 m and 20 km from the base and 100 m from each other. The first one is free; the others need an outpost radio.</p>
"""

BODY["grupo"] = """
<h2>Group</h2>
<p>With the <kbd>Group</kbd> icon, create a group or join one with its code. Up to 10 people.</p>
<ul>
<li>Quick alerts on the map: <kbd>HORDE HERE</kbd>, <kbd>LOOT HERE</kbd> and <kbd>HELP!</kbd>.</li>
<li>Group chat, and trading items side by side.</li>
<li>A single base for the group, with shared chests. When you join a group, your base is dismantled and what it held goes to the radio vault.</li>
<li>Roles in the group give more experience: <b>Doctor</b>, <b>Builder</b> and <b>Scout</b>.</li>
</ul>
<p>No one outside the group sees your name. To trade with anyone nearby (up to 40 m), use <kbd>Trade with someone here</kbd> in the menu.</p>

<h2>Stamps and the market</h2>
<p>The currency of the apocalypse is the <b>stamp</b>. Everyone's market is in the <b>mailbox</b> at the base or at the radio vault:</p>
<ul>
<li><kbd>Market</kbd>: buy and sell with other survivors. You have 6 slots; posting an offer costs 1 stamp and the seller pays a small fee. No one sees what others trade, only the reference price.</li>
<li><kbd>General store</kbd>: the counter sells the basics and buys anything cheap; it works even without internet.</li>
</ul>
<p>Stamps sitting idle above 300 lose a little each week. Dying costs 15% of them.</p>

<h2>Strongholds</h2>
<p>Big places (health, supermarket, restaurant, construction, gas station, police, firefighters, school) have a flag. Tap <kbd>Take the stronghold</kbd> and beat whoever is there in an arena with cars and barricades: at first it's bandits, many of them armed.</p>
<p>Win, and the stronghold is yours (or your group's) and pays 4 stamps a day. Leave up to 6 guards: each one takes one of your weapons (and the ammo). A guard who falls disappears with the weapon. With no guards, anyone takes it without a fight.</p>

<h2>Rescue flares</h2>
<p>Light a flare and hold out through the waves: easy (3), medium (4) or hard (5, with the Brute at the end). Win, and a rescue crate drops and you have 30 minutes to grab what you can.</p>
"""

BODY["corvo"] = """
<h2>The crow</h2>
<p>When you put the first door on your base, a crow lands on it. It stays. Only you can see it.</p>
<ul>
<li><b>Warns of the horde:</b> when many zombies are coming after you, it flies in from that direction, cawing.</li>
<li><b>Shows bodies:</b> circles piles of bodies that haven't been searched yet.</li>
<li><b>One place a day:</b> lands on an unlooted place nearby that gets one extra rare item.</li>
<li>It flies in from the direction of your group's alerts, and flees from loud noise.</li>
</ul>
<p>With the <kbd>Crow</kbd> button on the map, give it food to build a bond. With more trust it carries light things to the vault, points out special zombies, fetches a small item from the vault and, at the last level, caws to distract up to 3 zombies for a while. When it is hungry, it doesn't fly.</p>

<h2>Crow Radio</h2>
<p>With a radio in your backpack, in the chests or in the vault, open the menu → <kbd>Radio</kbd>:</p>
<ul>
<li><b>The week's horde:</b> announced from Monday, 30 to 60 zombies coming from one direction, on a night between Wednesday and Sunday. It crosses the region in a straight line, and the radio tells you if it passes near your base.</li>
<li><b>Supply drops:</b> 2 a week in the region, by day. They stay for 24 hours and their noise draws zombies for a while. Without a radio, you only hear about the ones very close by.</li>
<li><b>Tip of the day:</b> an unlooted place with one extra rare item.</li>
<li><b>Weekly mission:</b> take down, loot, walk or store planks, and earn stamps.</li>
<li>The phrase of the day, and alarms that go off around the city and pull the zombies.</li>
</ul>

<h2>Real weather and time</h2>
<ul>
<li><b>Rain:</b> muffles your noise, shortens your view, cools you and fills the barrel.</li>
<li><b>Fog:</b> shortens your view a lot.</li>
<li><b>Storm:</b> muffles noise more, but makes the zombies restless.</li>
<li><b>Night:</b> starts at the real sunset. In the small hours they get restless and hear better.</li>
<li><b>Full moon:</b> you see farther at night, but so do they, and more of them come out walking.</li>
</ul>
"""

BODY["memorias"] = """
<p>Around the city there are rare books that hold the last days of those who came before. Each one is a <b>memory</b>: a playable story, with a beginning, middle and end, and an outfit as a reward.</p>

<h2>Where to find them</h2>
<p>The books (<i>Memory: …</i>) are legendary and show up very rarely in the furniture <b>inside</b> places: only by going in, never through the door. Each memory comes from one kind of place:</p>
<ul>
<li><b>Old Jorge:</b> houses</li>
<li><b>The night shift:</b> health places</li>
<li><b>The crow's voice:</b> electronics stores</li>
<li><b>Thursday duty:</b> police stations</li>
<li><b>The vault:</b> military bunkers</li>
</ul>
<p>Once you've read a book, you won't find another one like it. If you find a duplicate, it becomes 3 stamps.</p>

<h2>Playing</h2>
<ol class="steps">
<li>In the backpack, tap the book and then <kbd>Put on the shelf</kbd>.</li>
<li>Go to an outpost or tent and enter the radio vault.</li>
<li>Open the <kbd>SHELF OF MEMORIES</kbd>, tap the spine and then <kbd>PLAY</kbd>. The session ends so the memory can begin.</li>
</ol>
<p>In a memory you play as someone else, with their kit; your character is kept safe and nothing that happens there touches them. If you fall before the end, the memory has failed: restart <kbd>FROM HERE</kbd> or <kbd>FROM THE START</kbd>. The shelf keeps your kill record.</p>

<h2>The seven memories</h2>
<ul>
<li><b>The last delivery:</b> the mail carrier on the night of the storm. Mail carrier outfit.</li>
<li><b>Old Jorge:</b> the doorman who locked up the building. Doorman outfit.</li>
<li><b>The night shift:</b> nurse Lúcia on the last shift in the ER. Nurse outfit.</li>
<li><b>The crow's voice:</b> radio host Rosa, who stayed on the air. Radio host headset, and the radio's phrase of the day is signed by her from then on.</li>
<li><b>Thursday duty:</b> Officer Ramos holding the police station. Police uniform.</li>
<li><b>The vault:</b> Private Nunes going down the bunker floor by floor. Military uniform.</li>
<li><b>The crow:</b> just flying and reading. It appears on the shelf after the other six have been played.</li>
</ul>
<div class="tip"><b>Ribbons on its leg</b>When you finish The crow, your crow starts wearing a ribbon from each memory.</div>
"""
