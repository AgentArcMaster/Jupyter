export const sampleCaseText = `Rahul met Arjun at Park Street.
Arjun transferred ₹50,000 to Vikram.
Vikram owns vehicle WB02AB1234.
Vikram contacted Sameer.
Sameer met Rahul at Park Street.`;

export const sampleCase = {
  entities: [
    { id: "p1", name: "Rahul", type: "PERSON" },
    { id: "p2", name: "Arjun", type: "PERSON" },
    { id: "p3", name: "Vikram", type: "PERSON" },
    { id: "p4", name: "Sameer", type: "PERSON" },
    { id: "l1", name: "Park Street", type: "LOCATION" },
    { id: "v1", name: "WB02AB1234", type: "VEHICLE" },
    { id: "m1", name: "₹50,000", type: "FINANCIAL" }
  ],

  relationships: [
    { source: "p1", target: "p2", type: "MET" },
    { source: "p2", target: "p3", type: "TRANSFERRED_MONEY" },
    { source: "p3", target: "v1", type: "OWNS" },
    { source: "p3", target: "p4", type: "CONTACTED" },
    { source: "p4", target: "p1", type: "MET" },
    { source: "p1", target: "l1", type: "VISITED" },
    { source: "p4", target: "l1", type: "VISITED" },
    { source: "p2", target: "m1", type: "TRANSFERRED" }
  ]
};