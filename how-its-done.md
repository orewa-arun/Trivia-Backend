1. ### commands for virtual env creation:

   python3 -m venv .venv
   source .venv/bin/activate

2. ### create schema, run:
   schema.sql and question_and_ad_insertion_script.sql

### TODOS:

- CREATE TABLE game_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  score INTEGER DEFAULT 0
  questions_attended INTEGER
  ad_questions_attended INTEGER
  quiz_questions_limit INTEGER (condition that questions_limit >= questions_attended)
  ad_questions_limit INTEGER (condition that ad_questions_limit >= ad_questions_attended)
  );

In this table we have to store no of questions attended by updating it everytime we are updating score, while submitting the answer.
While insertion of session while creating it, we ought to set the questions_limit, in that way when questions_attended should throw an error, we catch that error with a particular message in frontend, and then move to the next quizPhase.
