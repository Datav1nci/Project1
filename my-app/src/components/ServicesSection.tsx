import { Wrench, Building, HardHat } from "lucide-react";
import ServiceCard from "@/components/ServiceCard";

const data = [
  {
    title: "Génie structural",
    icon: <Building size={32} />,
    description:
      "Conception, analyse et réhabilitation de structures pour garantir sécurité et durabilité.",
  },
  {
    title: "Gestion de projets",
    icon: <Wrench size={32} />,
    description:
      "Planification complète et suivi rigoureux pour respecter budget et échéancier.",
  },
  {
    title: "Développement immobilier",
    icon: <HardHat size={32} />,
    description:
      "Accompagnement stratégique allant de l’étude de faisabilité à la réalisation clé en main.",
  },
];

export default function ServicesSection() {
  return (
    <section id="services" className="py-20">
      <h2 className="mb-12 text-center text-3xl font-bold">Nos services</h2>

      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {data.map((card) => (
          <ServiceCard key={card.title} {...card} />
        ))}
      </div>
    </section>
  );
}
