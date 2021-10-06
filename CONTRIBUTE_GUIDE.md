# Contribute Guide
This guide specifies the naming conventions used to contribute to this project.

## Commits
### Work on issues
#### Commit Titles
When commiting work, commit titles should have the following format:
<br>
`[#<issue-number>] <Short descriptive title>` (*Notice the # character before the issue-number*)
<br><br>
#### Commit Body
If the commit warrants more details than a short descriptive title, a body should be created with a bullet point formatted list of the work items included in the commit.
<br><br>
For example:
<br>
![image](https://user-images.githubusercontent.com/19224656/136252194-08672a72-ada7-47f8-a636-fa91c27b5ced.png)
<br><br>
This is a screen capture of a commit being created in vim. Notice that the tilte is sepatrated from the body by an empty line.
<br><br>
*Big brain move:*<br>
The `alt` code for a bullet character is: `0149`
### Work not related to issues
Commits should ALWAYS be associated with an issue!

## Pull Requests

## Branches
### Work on Sprint Tasks
Branches associated with issues that represent tasks in the Sprint Backlog are to be named as follows:
<br>
`<task-id>/<issue-number>`
<br><br>
For example:<br>
Assume issue #12 was created for task with id **EG-1-3**, then the corresponding branch will be named as follows:
<br>
`eg-1-3/12` (*Notice the letters are all small caps.*)
### Work on other issues
Branches associated with issues that do NOT represent tasks in the Sprint should be named as follows:
<br>
`<descriptive-title>/<issue-number>`
<br><br>
Where `<descriptive-title>` should be clear, concise, and representative of the goals associated with the issue.
<br><br>
For example:<br>
Assume issue #30 is related to documentation work where a UML diagram is to be added. A possible branch name could be:<br>
`doc/add-uml-diagram/30` (*Notice how 'doc/' categorizes the type of work being done.*)
### Work not related to issues
Branches should ALWAYS be associated with an issue!
