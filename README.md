# Language_models_explore_numeracy

Solving math word problems using language models is usually achieved by following one of the two methods
* Build an encoder decoder module to take in a math word problem as its input and output the answer directly
* Build an encoder decoder module to take in a math word problme as its input and output a neural symbolic expression which can be later passed to a separate program to get the final answer.

Example -
Input - A man swims downstream 96 km and upstream 40 km taking 8 hours each time ; what is the speed of the current ?
* Output by approach 1 - 3.5 km/hr
* Output by apporach 2 - divide n0 n2 divide n1 n2 subtract #0 #1 divide #2 const_2 ( this is equivalent to an instruction which can be fed to a program to solve for the correct answer)

In this project we aim to follow the 2nd approach and are using [MathQA](https://math-qa.github.io/) dataset.</br>
While working on the dataset we found that roughly 50% of the data has been incorrectly annotated.

| File          | Correctly annotated | Incorrectly annotated |
| ------------- | ------------------- |---------------------- |
| train.json    | 29837               | 15086                 |
| dev.json      | 4475                | 2234                  |
| test.json     | 2985                | 1476                  |

We aim to build a Fixer which can automatically correct these incorrectly annotated datapoints using self-supervision using the below steps.</br>
* Limit the dataset to only correctly annotated datapoints 
* Randomly perturb the correctly annotated datapoints and train a model which when given a math word problem and the pertubed datapoint can recover back the correct version
* Use the trained model to fix the incorrectly annotated datapoints


example - 
```
a man swims downstream 96 km and upstream 40 km taking 8 hours each time ; what is the speed of the current ? [SEP] divide n1 n2 divide n0 n2 add #0 #1 divide #2 const_2 -> divide n0 n2 divide n1 n2 subtract #0 #1 divide #2 const_2
```
Inputs
* a man swims downstream 96 km and upstream 40 km taking 8 hours each time ; what is the speed of the current ?
* [SEP] *(separator token)*
* divide n1 n2 divide n0 n2 add #0 #1 divide #2 const_2 *(perturbed symbolic expression)*

Output
* divide n0 n2 divide n1 n2 subtract #0 #1 divide #2 const_2 *(correct symbolic expression)*


So far we have used transformer based architecture from OpenNMT to achieve the below results.</br>
Note :  Accuracy in the results represents the percentage of incorrectly annotated expressions recovered from the training set


Rate of corruption : perturb 1 token per expression</br>
Steps : 10000
| Method            | Avg. accuracy |	seed 1	| seed 2	| seed 3 |
|------------------ |-------------- |-------- |-------- |------- |
| perturb 100% data |	16.27			    | 16.57	  | 16.05	  | 16.19  |	
| perturb 70% data 	|	16.11			    | 15.97	  | 16.2	  | 16.16  |	


Rate of corruption : perturb 2 tokens per expression</br>
Steps : 10000
| Method            | Avg. accuracy |	seed 1	| seed 2	| seed 3 |
|------------------ |-------------- |-------- |-------- |------- |
| perturb 100% data |	16.11			    | 16.39	  | 15.8	  | 16.13  |	
| perturb 70% data 	|	16.10			    | 16.48	  | 15.93	  | 15.9   |	

Rate of corruption : perturb 3 tokens per expression</br>
Steps : 10000
| Method            | Avg. accuracy |	seed 1	| seed 2	| seed 3 |
|------------------ |-------------- |-------- |-------- |------- |
| perturb 100% data |	16.10			    | 15.81	  | 16.17	  | 16.31  |	
| perturb 70% data 	|	16.42			    | 16.65   | 16  	  | 16.61  |	


