---
title: Analogy - The MAA island
layout: default
parent: What is MAA?
---

# The MAA Island

To illustrate the MAA concept, imagine you are stranded on an island, and you need to determine where to build a camp. The island has a freshwater lake, an area with coconut palms, an area with good hunting grounds and an area with dangerous predators.

### The optimal location

You know that freshwater is crucial, so you base your search around the availablility of freshwater. You end up at the lake, which is the *optimal* location based on freshwater availability. 

> The MAA method always starts by finding the *optimal* solution to a problem, and the *optimal* objective function value.

### Limiting your search

You have found the place with the best freshwater access, so this is where you camp, right? If your only concern is freshwater, then yes. But you think that in the vicinity, there might be a better place. To know your possibilities, you want to look around the island, but you limit your search to stay close enough to the lake that you can reach it in 30 minutes if you need water.

> In the MAA method, the *MGA constraint* limits the area to search, by setting a new constraint which says that the objective function value when searching can be greater than the *optimal* objective function value times by a percentage, such as 10%.

### Searching the island

You decide to search the island by walking in a direction until you've walked for 30 minutes, or you meet an obstacle. While doing so, you draw a map. When you've searched in one direction, you return to the lake, and search in another direction. This is time-consuming, but you discover many different areas. This way, you eventually map the surrounding area which is close to the *optimal* freshwater spot, aka. the *near-optimal* area. 

> In the MAA method, searching is done by changing the objective function to search away from the optimum. Eventually, this stops at either the *MGA constraint* or another constraint. This maps the *near-optimal space*.
> 
> In the MAA method, only select variables are used when searching, to limit the dimensionality. 

### Decision time

With your map of the *near-optimal area*, you can now decide where you want to camp. You have found that:

* The lake is at the edge of the area with predators, so staying there entails a small risk. 

* There is an area with good hunting grounds at a safe distance from the predators, but also the max distance away from the lake. 

* There is a large area with coconuts which makes for easy food, but this is quite close to the predator area.

So, now you have a lot of information to base you decision on. Do you play it safe and stay away from the predators? Do you prioritize being close to hunting grounds, coconuts or freshwater? Do you stay at the lake, now that you know how your vicinity looks? 

Maybe you decide that you're willing to walk further, and search again, this time walking for 60 minutes?

> In the MAA method, the *near-optimal space* contains a lot of information, and decisionmakers can now choose to prioritize some things over others, or move away from areas likely to be affected by something not considered, such as future political regulations.
