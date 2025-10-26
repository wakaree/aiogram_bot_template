import { Pool } from "pg";
import { dbConfig } from "../config/db";

export const pool = new Pool(dbConfig);

export const connectDB = async () => {
  try {
    await pool.connect();
    console.log("✅ Database connected successfully");
  } catch (error) {
    console.error("❌ Database connection failed:", error);
    throw Error("Database connection failed");
  }
};
