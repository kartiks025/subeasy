CREATE TABLE "user"
(
  user_id varchar(20) NOT NULL,
  name varchar(50),
  email varchar(50) NOT NULL,
  password varchar(64) NOT NULL,
  PRIMARY KEY (user_id),
  UNIQUE (email)
);

CREATE TABLE course
(
  course_id varchar(10) NOT NULL,
  name varchar(100) NOT NULL,
  PRIMARY KEY (course_id)
);

CREATE TABLE section
(
  sec_id bigserial NOT NULL,
  sec_name varchar(20) NOT NULL,
  semester varchar(10) NOT NULL,
  year int NOT NULL,
  course_id varchar(10) NOT NULL,
  num_assignments int default 0,
  PRIMARY KEY (sec_id),
  FOREIGN KEY (course_id) REFERENCES course(course_id)
      on delete cascade
      on update cascade
);

CREATE TABLE sec_user
(
  role varchar(10) NOT NULL,
  user_id varchar(20) NOT NULL,
  sec_id bigint NOT NULL,
  id bigserial NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (user_id, sec_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (sec_id) REFERENCES section(sec_id)
      on delete cascade
      on update cascade
);

CREATE TABLE deadline
(
  deadline_id bigserial NOT NULL,
  soft_deadline timestamp NOT NULL,
  hard_deadline timestamp NOT NULL,
  freezing_deadline timestamp NOT NULL,
  PRIMARY KEY (deadline_id)
);

CREATE TABLE resource_limit
(
  resource_limit_id bigserial NOT NULL,
  cpu_time int NOT NULL,
  clock_time int NOT NULL,
  memory_limit int NOT NULL,
  stack_limit int NOT NULL,
  open_files int NOT NULL,
  max_filesize int NOT NULL,
  PRIMARY KEY (resource_limit_id)
);

insert into resource_limit values(default,10,60,32768,8192,512,1024);

CREATE TABLE admin
(
  id varchar(20) NOT NULL,
  email varchar(50) NOT NULL,
  password varchar(64) NOT NULL,
  name varchar(50),
  PRIMARY KEY (id),
  UNIQUE (email)
);

CREATE TABLE assignment
(
  assignment_id bigserial NOT NULL,
  assignment_no int NOT NULL,
  title varchar(50) NOT NULL,
  description text,
  publish_time timestamp NOT NULL,
  visibility boolean NOT NULL default false,
  helper_file_name varchar(50),
  helper_file bytea,
  crib_deadline timestamp NOT NULL,
  sec_id bigint NOT NULL,
  deadline_id bigint NOT NULL,
  num_problems int NOT NULL default 1,
  PRIMARY KEY (assignment_id),
  FOREIGN KEY (sec_id) REFERENCES section(sec_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (deadline_id) REFERENCES deadline(deadline_id)
      on delete cascade
      on update cascade
);

CREATE TABLE assign_ip
(
  start_ip varchar(60) NOT NULL,
  end_ip varchar(60) NOT NULL,
  assignment_id bigint NOT NULL,
  id bigserial NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (start_ip, end_ip, assignment_id),
  FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id)
      on delete cascade
      on update cascade
);

CREATE TABLE problem
(
  problem_id bigserial NOT NULL,
  problem_no int NOT NULL,
  title varchar(50) NOT NULL,
  description text,
  helper_file_name varchar(50),
  helper_file bytea,
  solution_filename varchar(50),
  solution_file bytea,
  compile_cmd text,
  sol_visibility boolean NOT NULL default false,
  assignment_id bigint NOT NULL,
  resource_limit_id bigint NOT NULL,
  num_testcases int NOT NULL default 0,
  PRIMARY KEY (problem_id),
  FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (resource_limit_id) REFERENCES resource_limit(resource_limit_id)
      on delete cascade
      on update cascade
);

CREATE TABLE testcase
(
  problem_id bigint NOT NULL,
  testcase_no int NOT NULL,
  infile_name varchar(50) NOT NULL,
  infile bytea NOT NULL,
  outfile_name varchar(50) NOT NULL,
  outfile bytea NOT NULL,
  marks int NOT NULL default 1,
  visibility boolean NOT NULL default false,
  id bigserial NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (testcase_no, problem_id),
  FOREIGN KEY (problem_id) REFERENCES problem(problem_id)
      on delete cascade
      on update cascade
);

CREATE TABLE submission
(
  user_id varchar(50) NOT NULL,
  problem_id bigint NOT NULL,
  sub_no int NOT NULL,
  marks_auto int NOT NULL default 0,
  marks_inst int NOT NULL default 0,
  sub_file_name varchar(50) NOT NULL,
  sub_file bytea NOT NULL,
  id bigserial NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (sub_no, problem_id, user_id),
  FOREIGN KEY (problem_id) REFERENCES problem(problem_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
);

CREATE TABLE user_submissions
(
  user_id varchar(50) NOT NULL,
  problem_id bigint NOT NULL,
  num_submissions int NOT NULL,
  final_submission_no int NOT NULL default 0,
  id bigserial NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (user_id, problem_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (problem_id) REFERENCES problem(problem_id)
      on delete cascade
      on update cascade
);

CREATE TABLE crib
(
  crib_id bigserial NOT NULL,
  text text NOT NULL,
  resolved boolean NOT NULL default false,
  timestamp timestamp NOT NULL,
  user_id varchar(20) NOT NULL,
  problem_id bigint NOT NULL,
  CONSTRAINT user_prob UNIQUE (user_id, problem_id),
  PRIMARY KEY (crib_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (problem_id) REFERENCES problem(problem_id)
      on delete cascade
      on update cascade
);

CREATE TABLE comment
(
  comment_id bigserial NOT NULL,
  crib_id bigint NOT NULL,
  text text NOT NULL,
  timestamp timestamp NOT NULL,
  user_id varchar(20) NOT NULL,
  PRIMARY KEY (comment_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
      on delete cascade
      on update cascade,
  FOREIGN KEY (crib_id) REFERENCES crib(crib_id)
      on delete cascade
      on update cascade
);

CREATE TABLE reset_password
(
  uuid varchar(64) NOT NULL,
  timestamp timestamp NOT NULL,
  email varchar(50) NOT NULL,
  PRIMARY KEY (uuid),
  FOREIGN KEY (email) REFERENCES "user"(email)
      on delete cascade
      on update cascade,
  UNIQUE(email)
);