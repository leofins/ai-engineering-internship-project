import type { CreateExpressContextOptions } from "@trpc/server/adapters/express";
import type { User } from "../../drizzle/schema";
import { sdk } from "./sdk";

export type TrpcContext = {
  req: CreateExpressContextOptions["req"];
  res: CreateExpressContextOptions["res"];
  user: User | null;
};

export async function createContext(
  opts: CreateExpressContextOptions
): Promise<TrpcContext> {
  let user: User | null = null;

  try {
    user = await sdk.authenticateRequest(opts.req);
  } catch (error) {
    // If in development and authentication fails (no cookie), use mock user
    if (process.env.NODE_ENV === "development" || !process.env.NODE_ENV) {
      console.log("[Auth] Dev mode: Using mock user");
      user = {
        id: 1,
        openId: "mock-user-id",
        name: "Dev User",
        email: "dev@example.com",
        loginMethod: "mock",
        role: "admin",
        createdAt: new Date(),
        updatedAt: new Date(),
        lastSignedIn: new Date(),
      };
    } else {
      user = null;
    }
  }

  // Backup check: if sdk throws but returns undefined/null for user, force mock in dev
  if (!user && (process.env.NODE_ENV === "development" || !process.env.NODE_ENV)) {
      console.log("[Auth] Dev mode: Using mock user (fallback)");
      user = {
        id: 1,
        openId: "mock-user-id",
        name: "Dev User",
        email: "dev@example.com",
        loginMethod: "mock",
        role: "admin",
        createdAt: new Date(),
        updatedAt: new Date(),
        lastSignedIn: new Date(),
      };
  }

  return {
    req: opts.req,
    res: opts.res,
    user,
  };
}
