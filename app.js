let catalogData = { categories: [], products: [] };
let draftItems = [];
let selectedProduct = null;
let activeCategoryFilter = 'ALL';

// DOM Elements
const categorySelect = document.getElementById('categorySelect');
const crackerSelect = document.getElementById('crackerSelect');
const quantityInput = document.getElementById('quantityInput');
const btnQtyMinus = document.getElementById('btnQtyMinus');
const btnQtyPlus = document.getElementById('btnQtyPlus');

const productPreviewBox = document.getElementById('productPreviewBox');
const previewFactory = document.getElementById('previewFactory');
const previewUnitPrice = document.getElementById('previewUnitPrice');
const previewPerUnit = document.getElementById('previewPerUnit');
const previewCaseContent = document.getElementById('previewCaseContent');
const currentSelectionTotal = document.getElementById('currentSelectionTotal');

const btnAddItem = document.getElementById('btnAddItem');
const draftItemsList = document.getElementById('draftItemsList');
const btnClearDraft = document.getElementById('btnClearDraft');
const displayGrandTotal = document.getElementById('displayGrandTotal');

const orderForm = document.getElementById('orderForm');
const buyerNameInput = document.getElementById('buyerName');
const contactNumberInput = document.getElementById('contactNumber');
const btnPlaceOrder = document.getElementById('btnPlaceOrder');

const catalogSearchInput = document.getElementById('catalogSearchInput');
const categoryPillsBar = document.getElementById('categoryPillsBar');
const productCardsGrid = document.getElementById('productCardsGrid');

const metricCatalogCount = document.getElementById('metricCatalogCount');
const metricCategoryCount = document.getElementById('metricCategoryCount');

// Admin Modal Elements
const btnAdminDownload = document.getElementById('btnAdminDownload');
const adminModal = document.getElementById('adminModal');
const btnCloseAdminModal = document.getElementById('btnCloseAdminModal');
const btnCancelAdmin = document.getElementById('btnCancelAdmin');
const adminLoginForm = document.getElementById('adminLoginForm');
const adminUsernameInput = document.getElementById('adminUsername');
const adminPasswordInput = document.getElementById('adminPassword');

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
  fetchCatalog();
  setupEventListeners();
  setupAdminModal();
});

function setupEventListeners() {
  categorySelect.addEventListener('change', onCategoryChange);
  crackerSelect.addEventListener('change', onCrackerChange);
  
  quantityInput.addEventListener('input', updateSelectionTotal);
  btnQtyMinus.addEventListener('click', () => {
    let val = parseInt(quantityInput.value) || 1;
    if (val > 1) {
      quantityInput.value = val - 1;
      updateSelectionTotal();
    }
  });
  btnQtyPlus.addEventListener('click', () => {
    let val = parseInt(quantityInput.value) || 1;
    quantityInput.value = val + 1;
    updateSelectionTotal();
  });

  btnAddItem.addEventListener('click', addItemToDraft);
  btnClearDraft.addEventListener('click', clearDraft);
  orderForm.addEventListener('submit', handlePlaceOrder);

  catalogSearchInput.addEventListener('input', filterCatalogCards);
}

// Setup Owner Admin Login Modal
function setupAdminModal() {
  btnAdminDownload.addEventListener('click', () => {
    adminUsernameInput.value = '';
    adminPasswordInput.value = '';
    adminModal.style.display = 'flex';
  });

  btnCloseAdminModal.addEventListener('click', () => {
    adminModal.style.display = 'none';
  });

  btnCancelAdmin.addEventListener('click', () => {
    adminModal.style.display = 'none';
  });

  adminModal.addEventListener('click', (e) => {
    if (e.target === adminModal) {
      adminModal.style.display = 'none';
    }
  });

  adminLoginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const user = adminUsernameInput.value.trim();
    const pass = adminPasswordInput.value.trim();

    try {
      const res = await fetch('/api/admin/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
      });

      if (res.ok) {
        const data = await res.json();
        showToast('Owner Verified! Downloading Excel Workbook...', 'success');
        adminModal.style.display = 'none';
        window.location.href = `/api/download-excel?key=${encodeURIComponent(data.token)}`;
      } else {
        showToast('Invalid Owner Credentials!', 'error');
      }
    } catch (err) {
      showToast('Error verifying credentials', 'error');
    }
  });
}

// Fetch Catalog Data
async function fetchCatalog() {
  try {
    const res = await fetch('/api/catalog');
    catalogData = await res.json();
    
    // Populate Form Category Dropdown
    categorySelect.innerHTML = '<option value="">-- Choose Category --</option>';
    catalogData.categories.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = cat;
      categorySelect.appendChild(opt);
    });

    // Populate Category Pills Bar
    renderCategoryPills(catalogData.categories);

    metricCatalogCount.textContent = catalogData.products.length;
    metricCategoryCount.textContent = catalogData.categories.length;

    renderProductCards(catalogData.products);
  } catch (err) {
    showToast('Failed to load catalog', 'error');
  }
}

// Render Category Filter Pills
function renderCategoryPills(categories) {
  categoryPillsBar.innerHTML = '<button class="pill-btn active" data-category="ALL">All Categories</button>';
  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'pill-btn';
    btn.dataset.category = cat;
    btn.textContent = cat;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategoryFilter = cat;
      filterCatalogCards();
    });
    categoryPillsBar.appendChild(btn);
  });

  document.querySelector('.pill-btn[data-category="ALL"]').addEventListener('click', () => {
    document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.pill-btn[data-category="ALL"]').classList.add('active');
    activeCategoryFilter = 'ALL';
    filterCatalogCards();
  });
}

// Category Dropdown Change Handler
function onCategoryChange() {
  const chosenCat = categorySelect.value;
  crackerSelect.innerHTML = '<option value="">-- Choose Cracker --</option>';
  selectedProduct = null;
  if (productPreviewBox) productPreviewBox.style.display = 'none';

  if (!chosenCat) {
    crackerSelect.disabled = true;
    crackerSelect.innerHTML = '<option value="">-- Select Category First --</option>';
    updateSelectionTotal();
    return;
  }

  const filteredProducts = catalogData.products.filter(p => 
    p.category.trim().toLowerCase() === chosenCat.trim().toLowerCase()
  );

  if (filteredProducts.length === 0) {
    crackerSelect.disabled = true;
    crackerSelect.innerHTML = '<option value="">-- No Items In Category --</option>';
  } else {
    filteredProducts.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.item_id;
      opt.textContent = `${p.name} - ₹${p.price.toFixed(2)}`;
      crackerSelect.appendChild(opt);
    });
    crackerSelect.disabled = false;
  }

  updateSelectionTotal();
}

// Cracker Dropdown Change Handler
function onCrackerChange() {
  const chosenItemId = crackerSelect.value;
  const previewImage = document.getElementById('previewImage');

  selectedProduct = catalogData.products.find(p => p.item_id === chosenItemId) || null;

  if (selectedProduct && productPreviewBox) {
    if (previewFactory) previewFactory.textContent = "AADHAN FIRE WORKS";
    if (previewUnitPrice) previewUnitPrice.textContent = `₹${selectedProduct.price.toFixed(2)}`;
    if (previewPerUnit) previewPerUnit.textContent = selectedProduct.per || '1 Unit';
    if (previewCaseContent) previewCaseContent.textContent = selectedProduct.case_content || '-';
    if (previewImage) previewImage.src = selectedProduct.image_url;
    productPreviewBox.style.display = 'block';
  } else if (productPreviewBox) {
    productPreviewBox.style.display = 'none';
  }

  updateSelectionTotal();
}

// Update current selection total calculation
function updateSelectionTotal() {
  const qty = parseInt(quantityInput.value) || 0;
  let price = selectedProduct ? selectedProduct.price : 0;
  let subtotal = price * qty;
  currentSelectionTotal.textContent = `₹${subtotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  updateGrandTotal();
}

// Select item directly from Product Card click
function selectProductFromCard(itemId) {
  const item = catalogData.products.find(p => p.item_id === itemId);
  if (!item) return;

  categorySelect.value = item.category;
  onCategoryChange();
  crackerSelect.value = item.item_id;
  onCrackerChange();

  showToast(`Selected: ${item.name}`);
  orderForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Render Product Cards Grid with Big Thumbnail Images
function renderProductCards(products) {
  if (products.length === 0) {
    productCardsGrid.innerHTML = `
      <div class="loading-cards">
        <i class="fa-solid fa-box-open"></i> No firecrackers found matching your filter.
      </div>
    `;
    return;
  }

  productCardsGrid.innerHTML = '';
  products.forEach(p => {
    const card = document.createElement('div');
    card.className = 'product-card-item';
    card.innerHTML = `
      <div class="card-img-wrapper">
        <img src="${p.image_url}" alt="${p.name}" class="card-product-img" loading="lazy">
        <span class="card-category-badge">${p.category}</span>
        <span class="card-id-tag">${p.item_id}</span>
      </div>
      <div class="card-body">
        <h4 class="card-title">${p.name}</h4>
        <div class="card-meta">
          <span><i class="fa-solid fa-box"></i> Per: ${p.per || '1 Unit'}</span>
          <span><i class="fa-solid fa-cubes"></i> Case: ${p.case_content || '-'}</span>
        </div>
        <div class="card-price-row">
          <span class="card-price-tag">₹${p.price.toFixed(2)}</span>
          <button type="button" class="btn-card-select" onclick="selectProductFromCard('${p.item_id}')">
            <i class="fa-solid fa-cart-plus"></i> Select Item
          </button>
        </div>
      </div>
    `;
    productCardsGrid.appendChild(card);
  });
}

// Filter Catalog Cards Grid
function filterCatalogCards() {
  const query = catalogSearchInput.value.toLowerCase().trim();
  
  let filtered = catalogData.products;

  if (activeCategoryFilter && activeCategoryFilter !== 'ALL') {
    filtered = filtered.filter(p => p.category === activeCategoryFilter);
  }

  if (query) {
    filtered = filtered.filter(p =>
      p.item_id.toLowerCase().includes(query) ||
      p.category.toLowerCase().includes(query) ||
      p.name.toLowerCase().includes(query)
    );
  }

  renderProductCards(filtered);
}

// Add Item to Order Draft List
function addItemToDraft() {
  if (!selectedProduct) {
    showToast('Please select a cracker category and item first', 'error');
    return;
  }
  const qty = parseInt(quantityInput.value) || 0;
  if (qty <= 0) {
    showToast('Please enter a valid quantity', 'error');
    return;
  }

  const subtotal = selectedProduct.price * qty;
  draftItems.push({
    category: selectedProduct.category,
    cracker_name: selectedProduct.name,
    unit_price: selectedProduct.price,
    quantity: qty,
    subtotal: subtotal
  });

  renderDraftList();
  showToast(`Added ${selectedProduct.name} (x${qty}) to draft`);
  
  // Reset cracker dropdown
  crackerSelect.value = '';
  onCrackerChange();
  quantityInput.value = 1;
  updateSelectionTotal();
}

function renderDraftList() {
  if (draftItems.length === 0) {
    draftItemsList.innerHTML = `
      <div class="empty-draft-msg">
        <i class="fa-solid fa-basket-shopping"></i> Select a cracker above or tap any product card below to add items.
      </div>
    `;
    btnClearDraft.style.display = 'none';
  } else {
    draftItemsList.innerHTML = '';
    draftItems.forEach((item, idx) => {
      const div = document.createElement('div');
      div.className = 'draft-item-row';
      div.innerHTML = `
        <div class="draft-item-info">
          <span class="draft-item-title">${item.cracker_name}</span>
          <span class="draft-item-meta">${item.category} | Qty: ${item.quantity} x ₹${item.unit_price.toFixed(2)}</span>
        </div>
        <div style="display:flex; align-items:center;">
          <span class="draft-item-subtotal">₹${item.subtotal.toFixed(2)}</span>
          <button type="button" class="btn-remove-item" onclick="removeDraftItem(${idx})"><i class="fa-solid fa-trash"></i></button>
        </div>
      `;
      draftItemsList.appendChild(div);
    });
    btnClearDraft.style.display = 'block';
  }

  updateGrandTotal();
}

function removeDraftItem(idx) {
  draftItems.splice(idx, 1);
  renderDraftList();
}

function clearDraft() {
  draftItems = [];
  renderDraftList();
}

function updateGrandTotal() {
  let total = 0;
  if (draftItems.length > 0) {
    total = draftItems.reduce((acc, i) => acc + i.subtotal, 0);
  } else if (selectedProduct) {
    const qty = parseInt(quantityInput.value) || 0;
    total = selectedProduct.price * qty;
  }
  displayGrandTotal.textContent = `₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
}

// Handle Order Submission to Server
async function handlePlaceOrder(e) {
  e.preventDefault();

  const buyer = buyerNameInput.value.trim();
  const contact = contactNumberInput.value.trim();

  if (!buyer || !contact) {
    showToast('Please fill in Buyer Name and Contact Number', 'error');
    return;
  }

  let payload = {
    buyer_name: buyer,
    contact_number: contact,
    items: []
  };

  if (draftItems.length > 0) {
    payload.items = draftItems;
  } else if (selectedProduct) {
    const qty = parseInt(quantityInput.value) || 1;
    payload.items = [{
      category: selectedProduct.category,
      cracker_name: selectedProduct.name,
      unit_price: selectedProduct.price,
      quantity: qty
    }];
  } else {
    showToast('Please select at least one cracker item to order', 'error');
    return;
  }

  btnPlaceOrder.disabled = true;
  btnPlaceOrder.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving to Excel...';

  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Success! Order recorded in Excel (Total: ₹${data.grand_total.toFixed(2)})`, 'success');
      
      // Reset form & draft
      draftItems = [];
      renderDraftList();
      categorySelect.value = '';
      onCategoryChange();
      buyerNameInput.value = '';
      contactNumberInput.value = '';
    } else {
      showToast(data.detail || 'Error placing order', 'error');
    }
  } catch (err) {
    showToast('Network error while placing order', 'error');
  } finally {
    btnPlaceOrder.disabled = false;
    btnPlaceOrder.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Place Order & Save to Excel';
  }
}

// Toast System
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
