export default function LBHEnterprise() {
  // TU PAYPAL YA EXISTE - lo tomamos del FUNDING
  const paypalEnterprise = "https://www.paypal.com/paypalme/hormigasais/100"; 
  // Si tu paypalme es otro, cámbialo aquí
  const stripeEnterprise = "https://buy.stripe.com/test_100_enterprise"; // REEMPLAZA con tu link real de Stripe cuando lo crees

  return (
    <div className="border border-yellow-400/30 bg-black/50 p-6 rounded-2xl my-8">
      <h3 className="text-yellow-400 text-xl font-bold">LBH Enterprise — $100+ / mes</h3>
      <p className="text-gray-300 text-sm mt-2">
        Sellos ilimitados + API privada + Certificado PDF con sello jurídico.
        Facturación directa, sin comisión GitHub. Acepta débito local SV.
      </p>
      <div className="flex gap-3 mt-4">
        <a href={paypalEnterprise} target="_blank" 
           className="px-5 py-3 bg-[#FFC439] text-black font-bold rounded-xl hover:bg-yellow-300">
          Pagar con PayPal / Débito Local
        </a>
        <a href={stripeEnterprise} target="_blank"
           className="px-5 py-3 bg-white text-black font-bold rounded-xl hover:bg-gray-200">
          Pagar con Tarjeta (Stripe)
        </a>
      </div>
      <p className="text-xs text-gray-500 mt-3">Protocolo LBH v2.0 · Nodo A16 · Operado desde El Salvador</p>
    </div>
  );
}
