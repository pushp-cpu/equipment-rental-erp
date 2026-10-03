"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    {
      name: "Dashboard",
      path: "/dashboard",
    },
    {
      name: "Equipment",
      path: "/equipment",
    },
    {
      name: "Customers",
      path: "/customers",
    },
    {
      name: "Rentals",
      path: "/rentals",
    },
  ];

  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white flex flex-col">

      <div className="px-6 py-6 border-b border-slate-700">
        <h1 className="text-xl font-bold">
          Equipment Rental
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          ERP System
        </p>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">

        {links.map((link) => {
          const active = pathname === link.path;

          return (
            <Link
              key={link.path}
              href={link.path}
              className={`block rounded-lg px-4 py-3 transition ${
                active
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`}
            >
              {link.name}
            </Link>
          );
        })}

      </nav>

      <div className="px-4 py-6 border-t border-slate-700">

        <button
          onClick={() => {
            localStorage.removeItem("access_token");
            window.location.href = "/";
          }}
          className="w-full rounded-lg px-4 py-3 text-left text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          Logout
        </button>

      </div>

    </aside>
  );
}