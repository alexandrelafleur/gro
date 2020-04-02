
// Author: Francois Grondin
// Date: March 17th, 2020

// +----------------------------------------------------------------+
// | Scheduler (do not modify this section, except scheduler_run)   |
// +----------------------------------------------------------------+

// This holds all the information on a given task
typedef struct task_
{

  int priority;
  int period;
  int counter;
  void (*fcn)(void);

} Task;

// We limit the max number of tasks to 10
const int nMaxTasks = 10;
int nTasks = 0;
Task tasks[nMaxTasks];
const int NPINS = 5;
int pins[NPINS] = {2, 3, 4, 5, 6};
int volt = 0;

// Initialize the scheduler
void scheduler_init(void)
{

  for (int iTask = 0; iTask < nMaxTasks; iTask++)
  {
    tasks[iTask].priority = -1;
    tasks[iTask].period = -1;
    tasks[iTask].counter = 0;
    tasks[iTask].fcn = NULL;
  }
}

// Add a task
//
// Priority: A non-negative number that defines the priority of execution.
//           The larger the number, the higher the priority
// Period:   Period (in number of ticks) at which the task is called.
// Fcn:      Pointer to the function that gets called when the task is active.
//
void scheduler_add(int priority_, int period_, void (*fcn_)(void))
{

  if (nTasks < nMaxTasks)
  {
    tasks[nTasks].priority = priority_;
    tasks[nTasks].period = period_;
    tasks[nTasks].counter = 0;
    tasks[nTasks].fcn = fcn_;
    nTasks++;
  }
}

// Generate a tick on the scheduler
void scheduler_tick(void)
{

  for (int iTask = 0; iTask < nTasks; iTask++)
  {
    tasks[iTask].counter++;
  }
}

// Given the current tick, check if one or many tasks need to be executed.
// If multiple tasks need to start, start the one with the highest priority.
void scheduler_run(void)
{

  int iTaskToExecute = -1;

  int minPriority = 256;
  for (int i = 0; i < nTasks; i++)
  {

    if (tasks[i].priority < minPriority && tasks[i].priority >= 0)
    {
      if (tasks[i].counter > 0)
      {
        minPriority = tasks[i].priority;
        iTaskToExecute = i;
      }
    }

    if (tasks[i].counter > tasks[i].period)
    {
      tasks[i].counter = 0;
    }
  }

  // You need to code this part here to decide which task index
  // (iTaskToExecute) will be chosen (if no task need to be executed,
  // simply leave iTaskToExecute = -1)

  if (iTaskToExecute != -1)
  {
    tasks[iTaskToExecute].fcn();
    tasks[iTaskToExecute].counter -= tasks[iTaskToExecute].period;
  }
  scheduler_tick();
}

// +----------------------------------------------------------------+
// | Interrupts (do not modify this section)                        |
// +----------------------------------------------------------------+

void init_interrupts(void)
{

  // Configure the TIMER1 to raise an interrupt
  // every 5 msecs.
  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  OCR1A = 78;
  TCCR1B |= (1 << WGM12);
  TCCR1B |= (1 << CS12) | (1 << CS10);
  TIMSK1 |= (1 << OCIE1A);
  sei();
}

ISR(TIMER1_COMPA_vect)
{

  // This is called every 5 msecs.
  scheduler_tick();
}

// +----------------------------------------------------------------+
// | Tasks (This section will be modified)                          |
// +----------------------------------------------------------------+

void task0(void)
{
  static bool stateLed = true;
  stateLed = !stateLed;
  digitalWrite(pins[0], stateLed);
}

void task1(void)
{
  static bool stateLed = true;
  stateLed = !stateLed;
  digitalWrite(pins[1], stateLed);
}

void task2(void)
{
  static bool stateLed = true;
  stateLed = !stateLed;
  digitalWrite(pins[2], stateLed);
}

void task3(void)
{
  static bool stateLed = true;
  stateLed = !stateLed;
  digitalWrite(pins[3], stateLed);
}

void task4(void)
{
  static bool stateLed = true;
  stateLed = !stateLed;
  digitalWrite(pins[4], stateLed);
}

void taskPriority()
{
  volt = (analogRead(A0) - 1) * 5 / 1024;
  tasks[0].priority = 0;
  tasks[1].priority = volt >= 1 ? 1 : -1;
  tasks[2].priority = volt >= 2 ? 2 : -1;
  tasks[3].priority = volt >= 3 ? 3 : -1;
  tasks[4].priority = volt >= 4 ? 4 : -1;
}

// +----------------------------------------------------------------+
// | Initialization (This section will be modified)                 |
// +----------------------------------------------------------------+
void init_pin()
{
  for (int i = 0; i < NPINS; i++)
  {
    pinMode(pins[i], OUTPUT);
  }
  pinMode(A0, INPUT);
}

void setup()
{
  scheduler_init();
  // Task0 will be called every 200 ticks, with priority 0
  scheduler_add(0, 200 / 2, &task0);
  scheduler_add(1, 250 / 2, &task1);
  scheduler_add(2, 333 / 2, &task2);
  scheduler_add(3, 500 / 2, &task3);
  scheduler_add(4, 1000 / 2, &task4);
  scheduler_add(5, 100, &taskPriority);
  init_interrupts();
}

// +----------------------------------------------------------------+
// | Maintenance (do not modify this section)                       |
// +----------------------------------------------------------------+

void loop()
{
  scheduler_run();
  delay(1); // This is added to give the simulator a little break
}
