import { MigrationBuilder } from "node-pg-migrate";

export const up = (pgm: MigrationBuilder) => {
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
    id: {
      type: "uuid",
      primaryKey: true,
      default: pgm.func("gen_random_uuid()"),
    },
  });

  pgm.createTable("tasks", {
    id: {
      type: "uuid",
      primaryKey: true,
      default: pgm.func("gen_random_uuid()"),
    },
    user_id: {
      type: "uuid",
      notNull: true,
      references: "users",
      onDelete: "CASCADE",
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

  pgm.createIndex("tasks", "user_id");
  pgm.createIndex("scheduled_time", "task_id");
};

export const down = (pgm: MigrationBuilder) => {
  pgm.dropTable("scheduled_time");
  pgm.dropTable("tasks");
  pgm.dropTable("users");
  pgm.dropType("day_enum");
};
