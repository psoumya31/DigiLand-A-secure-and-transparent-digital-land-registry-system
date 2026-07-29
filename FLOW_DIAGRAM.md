```
🔄 COMPLETE LAND TRANSFER FLOW
==============================

STEP 1: BUYER REQUESTS
━━━━━━━━━━━━━━━━━━━━━━
  Buyer goes to "Buy Land" page
  ↓
  Sees listed properties (forSale: true)
  ↓
  Clicks "📩 Request Purchase"
  ↓
  POST /api/request/create
  ↓
  Creates Request with status = "pending"
  ↓
  SELLER GETS NOTIFICATION ✉️
  

STEP 2: SELLER REVIEWS & CONFIRMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Seller receives notification
  ↓
  Goes to "My Requests" page
  ↓
  Sees incoming request from Buyer
  ↓
  Reviews buyer details (name, email, wallet)
  ↓
  Clicks "✅ Confirm Transfer" button
  ↓
  PUT /api/request/seller-confirm/:id
  ↓
  Updates status = "seller_confirmed"
  ↓
  ADMIN GETS NOTIFICATION ✉️
  

STEP 3: ADMIN VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━
  Admin receives notification
  ↓
  Goes to "Pending Approvals"
  ↓
  Sees seller-confirmed requests
  ↓
  Badge shows "✓ Seller Confirmed"
  ↓
  Admin reviews:
    • Buyer identity ✓
    • Seller identity ✓
    • Land details ✓
    • Wallet addresses ✓
  ↓
  Clicks "✅ Approve & Transfer"
  ↓
  PUT /api/admin/approve/:id
  ↓
  

STEP 4: SMART CONTRACT EXECUTES (AUTOMATIC)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⛓️ Blockchain transfers land to buyer wallet
  ↓
  💾 MongoDB updated - ownerUserId = buyer
  ↓
  🔄 Land history recorded (from seller → to buyer)
  ↓
  📱 QR code regenerated with new owner
  ↓
  📧 Email notifications sent to BOTH
  ↓
  🔔 In-app notifications created
  ↓
  Request status = "approved"
  

FINAL RESULT:
━━━━━━━━━━━━
  ✅ Buyer owns the land
  ✅ Seller no longer owns the land
  ✅ Admin approved the transfer
  ✅ Blockchain recorded forever
  ✅ Both parties notified
  ✅ Certificate generated with QR code


DATA FLOW:
══════════════════════════════════════════════════════════════

┌─────────────────────┐
│    BUYER            │
│  (My Requests)      │
│  Status: Pending    │──────────┐
│                     │          │
└─────────────────────┘          │
                                 │
                    ┌────────────▼──────────┐
                    │   REQUEST OBJECT      │
                    │ {                     │
                    │  landId: "LAND-001"   │
                    │  buyerId: "123"       │──────┐
                    │  sellerId: "456"      │      │
                    │  status: "pending"    │      │
                    │ }                     │      │
                    └────────────┬──────────┘      │
                                 │                 │
                    ┌────────────▼─────────┐       │
                    │     SELLER SEES      │       │
                    │   (My Requests)      │       │
                    │ ✓ Buyer name         │       │
                    │ ✓ Buyer email        │       │
                    │ ✓ Buyer wallet       │       │
                    │ [Confirm Transfer]   │       │
                    └────────────┬─────────┘       │
                                 │                 │
                    ┌────────────▼─────────┐       │
                    │  Request Updated:    │       │
                    │ status: "seller_conf"│       │
                    │ sellerConfirmedAt: NN│       │
                    └────────────┬─────────┘       │
                                 │                 │
                    ┌────────────▼──────────────┐  │
                    │  ADMIN SEES IN:           │  │
                    │  Pending Approvals        │  │
                    │  - Buyer: ${buyer.name}   │  │
                    │  - Seller: ${seller.name} │  │
                    │  [Approve & Transfer]     │  │
                    └────────────┬──────────────┘  │
                                 │                 │
┌────────────────────────────────▼──────────────────────┐
│             BLOCKCHAIN EXECUTES                       │
│  smart contract transferLandOnChain()               │
│  Previous Owner: seller.walletAddress               │
│  New Owner: buyer.walletAddress                     │
│  ✓ Tx Hash saved in DB                             │
└────────────────────────────────┬─────────────────────┘
                                 │
                    ┌────────────▼─────────┐
                    │  LAND OBJECT UPDATED:│
                    │ ownerUserId: buyer   │
                    │ ownerWalletAddress   │
                    │ history: [...]       │
                    │ qrCode: regenerated  │
                    │ status: approved     │
                    └────────────┬─────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
        ┌───────▼─────┐   ┌─────▼───────┐   ┌───▼────────┐
        │    BUYER    │   │   SELLER    │   │   ADMIN    │
        │ Gets Email  │   │ Gets Email  │   │ Logged     │
        │ ✓ New owner │   │ ✓ Sold to   │   │ ✓ Approved │
        │ ✓ QR code   │   │ ✓ Price     │   │            │
        └─────────────┘   └─────────────┘   └────────────┘
```

DATABASE STATUS AT EACH STEP:
═════════════════════════════════════════════════════════════

Request Model:
- STEP 1: status = "pending" (request created)
- STEP 2: status = "seller_confirmed" (seller agreed)
- STEP 4: status = "approved" (admin approved + blockchain done)

Land Model:
- STEP 1-3: ownerUserId = seller (no change)
- STEP 4: ownerUserId = buyer (TRANSFERRED!)
          forSale = false (auto-removed from marketplace)
