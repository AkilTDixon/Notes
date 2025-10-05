@echo off

start cmd /k "MyEnv\Scripts\activate && python ToDoList.py"

start cmd /k "cd Frontend\frontend && npm run dev"
