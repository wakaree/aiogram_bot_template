start = Hi, how can I /help you?

startCreateTask =  Enter title
enterDescriptionTaskTitle =
    Please enter a description for your task:

    🏷️ *Title:* { $title }

enterRegularTime =
    Select the number of reminder repetitions:

    🏷️ *Title:* { $title }
    📝 *Description:* { $description }

chooseDayCreateTask =
    Select the day of reminder repetitions:

    🏷️ *Title:* { $title }
    📝 *Description:* { $description }
    📝 *disposable:* { $disposable } 

chooseDay =
    Select the day of reminder repetitions:

chooseTime =
    Please enter a time for your repetitions: 

    🏷️ *Day:* { $day }

scheduledTimes =
    Please enter a time for your repetitions: 

    🏷️ *Day:* { $day }
    🏷️ *Times:* { $times } 

createdTask = ✅ Task “{ $title }” has been successfully created!
  { $disposable ->
      [true] ♻️ This is a one-time task.
      [false] 🔁 This is a recurring task.
     *[other]
  }
  📅 Schedule:
  { $schedule }

# button 
startButtonChooseAction = Create task
watchButtonChooseAction = Watch tasks


# button create task
regularButtonChooseAction = Constantly
oneTimeButtonChooseAction = One time

# button chooseDay
createTaskTime = Create  
createTaskMondayButtonChooseAction = Monday 
createTaskMondayButtonChooseAction = Monday
createTaskTuesdayButtonChooseAction = Tuesday
createTaskWednesdayButtonChooseAction = Wednesday
createTaskThursdayButtonChooseAction = Thursday
createTaskFridayButtonChooseAction = Friday
createTaskSaturdayButtonChooseAction = Saturday
createTaskSundayButtonChooseAction = Sunday

