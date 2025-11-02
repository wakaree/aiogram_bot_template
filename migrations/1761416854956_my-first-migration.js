exports.up = (pgm) => {
  pgm.createType("day_enum", [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ]);

  pgm.createTable("users", {
    telegram_id: { type: "int", primaryKey: true },
    username: { type: "text" },
    first_name: { type: "text" },
    last_name: { type: "text" },
    created_at: {
      type: "timestamp",
      notNull: true,
      default: pgm.func("NOW()"),
    },
  });
  pgm.createTable("user_chats", {
    chat_id: { type: "int", primaryKey: true },
    user_id: {
      type: "int",
      notNull: true,
      references: "users(telegram_id)",
      onDelete: "CASCADE",
    },
  });

  pgm.createTable("tasks", {
    id: {
      type: "uuid",
      primaryKey: true,
      default: pgm.func("gen_random_uuid()"),
    },
    user_chats_id: {
      type: "int",
      notNull: true,
      references: "user_chats(chat_id)",
      onDelete: "CASCADE",
    },
    disposable: {
      type: "boolean",
      notNull: true,
      default: false,
    },
    title: { type: "text", notNull: true },
    description: { type: "text" },
    created_at: {
      type: "timestamp",
      notNull: true,
      default: pgm.func("current_timestamp"),
    },
  });

  pgm.createTable("scheduled_time", {
    id: {
      type: "uuid",
      primaryKey: true,
      default: pgm.func("gen_random_uuid()"),
    },
    task_id: {
      type: "uuid",
      notNull: true,
      references: "tasks",
      onDelete: "CASCADE",
    },
    day: { type: "day_enum", notNull: true },
    time_slots: { type: "text[]", notNull: true },
  });

  pgm.createIndex("user_chats", "user_id");
  pgm.createIndex("tasks", "user_chats_id");
  pgm.createIndex("scheduled_time", "task_id");
};

exports.down = (pgm) => {
  pgm.dropTable("scheduled_time");
  pgm.dropTable("tasks");
  pgm.dropTable("users");
  pgm.dropTable("users_chats");
  pgm.dropType("day_enum");
};
