import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-10">
      <div className="mx-auto max-w-7xl grid gap-8 px-4 md:grid-cols-2">
        <div>
          <h3 className="text-2xl font-bold text-white">Metanova</h3>
          <p className="mt-2 text-sm">
            © 2025 Metanova. Tous droits réservés.
          </p>
        </div>

        <nav className="flex flex-col gap-2 md:items-end">
          {["Accueil", "Services", "Projets", "À Propos", "Contact"].map((l) => (
            <Link key={l} href={`#${l.toLowerCase().replace(" ", "")}`} className="hover:text-white">
              {l}
            </Link>
          ))}
          <Link
            href="https://www.linkedin.com/company/metanova"
            target="_blank"
            className="mt-2 inline-block text-blue-400 hover:text-blue-300"
          >
            LinkedIn
          </Link>
        </nav>
      </div>
    </footer>
  );
}
