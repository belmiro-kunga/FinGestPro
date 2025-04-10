/**
 * IPC Handlers for the main process
 * This file contains all the IPC event handlers for communication between
 * the main process and renderer process
 */

// Product handlers
function setupProductHandlers(ipcMain, db) {
  // Get all products
  ipcMain.handle('get-products', async () => {
    try {
      const products = await db.all('SELECT * FROM products');
      return { success: true, data: products };
    } catch (error) {
      console.error('Error getting products:', error);
      return { success: false, error: error.message };
    }
  });

  // Get a single product by ID
  ipcMain.handle('get-product', async (event, id) => {
    try {
      const product = await db.get('SELECT * FROM products WHERE id = ?', [id]);
      return { success: true, data: product };
    } catch (error) {
      console.error('Error getting product:', error);
      return { success: false, error: error.message };
    }
  });

  // Add a new product
  ipcMain.handle('add-product', async (event, product) => {
    try {
      const result = await db.run(
        'INSERT INTO products (name, description, price, stock, category_id) VALUES (?, ?, ?, ?, ?)',
        [product.name, product.description, product.price, product.stock, product.category_id]
      );
      return { success: true, data: { id: result.lastID } };
    } catch (error) {
      console.error('Error adding product:', error);
      return { success: false, error: error.message };
    }
  });

  // Update a product
  ipcMain.handle('update-product', async (event, product) => {
    try {
      await db.run(
        'UPDATE products SET name = ?, description = ?, price = ?, stock = ?, category_id = ? WHERE id = ?',
        [product.name, product.description, product.price, product.stock, product.category_id, product.id]
      );
      return { success: true };
    } catch (error) {
      console.error('Error updating product:', error);
      return { success: false, error: error.message };
    }
  });

  // Delete a product
  ipcMain.handle('delete-product', async (event, id) => {
    try {
      await db.run('DELETE FROM products WHERE id = ?', [id]);
      return { success: true };
    } catch (error) {
      console.error('Error deleting product:', error);
      return { success: false, error: error.message };
    }
  });
}

// Sale handlers
function setupSaleHandlers(ipcMain, db) {
  // Create a new sale
  ipcMain.handle('create-sale', async (event, saleData) => {
    try {
      // Start a transaction
      await db.run('BEGIN TRANSACTION');
      
      // Insert the sale
      const saleResult = await db.run(
        'INSERT INTO sales (customer_id, total_amount, payment_method, created_at) VALUES (?, ?, ?, datetime("now"))',
        [saleData.customer_id, saleData.total_amount, saleData.payment_method]
      );
      
      const saleId = saleResult.lastID;
      
      // Insert sale items
      for (const item of saleData.items) {
        await db.run(
          'INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
          [saleId, item.product_id, item.quantity, item.price]
        );
        
        // Update product stock
        await db.run(
          'UPDATE products SET stock = stock - ? WHERE id = ?',
          [item.quantity, item.product_id]
        );
      }
      
      // Commit the transaction
      await db.run('COMMIT');
      
      return { success: true, data: { id: saleId } };
    } catch (error) {
      // Rollback in case of error
      await db.run('ROLLBACK');
      console.error('Error creating sale:', error);
      return { success: false, error: error.message };
    }
  });

  // Get all sales
  ipcMain.handle('get-sales', async () => {
    try {
      const sales = await db.all(`
        SELECT s.*, c.name as customer_name 
        FROM sales s 
        LEFT JOIN customers c ON s.customer_id = c.id 
        ORDER BY s.created_at DESC
      `);
      return { success: true, data: sales };
    } catch (error) {
      console.error('Error getting sales:', error);
      return { success: false, error: error.message };
    }
  });

  // Get sale details
  ipcMain.handle('get-sale-details', async (event, saleId) => {
    try {
      const sale = await db.get(`
        SELECT s.*, c.name as customer_name 
        FROM sales s 
        LEFT JOIN customers c ON s.customer_id = c.id 
        WHERE s.id = ?
      `, [saleId]);
      
      const items = await db.all(`
        SELECT si.*, p.name as product_name 
        FROM sale_items si 
        JOIN products p ON si.product_id = p.id 
        WHERE si.sale_id = ?
      `, [saleId]);
      
      return { success: true, data: { ...sale, items } };
    } catch (error) {
      console.error('Error getting sale details:', error);
      return { success: false, error: error.message };
    }
  });
}

// Customer handlers
function setupCustomerHandlers(ipcMain, db) {
  // Get all customers
  ipcMain.handle('get-customers', async () => {
    try {
      const customers = await db.all('SELECT * FROM customers ORDER BY name');
      return { success: true, data: customers };
    } catch (error) {
      console.error('Error getting customers:', error);
      return { success: false, error: error.message };
    }
  });

  // Add a new customer
  ipcMain.handle('add-customer', async (event, customer) => {
    try {
      const result = await db.run(
        'INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)',
        [customer.name, customer.email, customer.phone, customer.address]
      );
      return { success: true, data: { id: result.lastID } };
    } catch (error) {
      console.error('Error adding customer:', error);
      return { success: false, error: error.message };
    }
  });

  // Update a customer
  ipcMain.handle('update-customer', async (event, customer) => {
    try {
      await db.run(
        'UPDATE customers SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?',
        [customer.name, customer.email, customer.phone, customer.address, customer.id]
      );
      return { success: true };
    } catch (error) {
      console.error('Error updating customer:', error);
      return { success: false, error: error.message };
    }
  });

  // Delete a customer
  ipcMain.handle('delete-customer', async (event, id) => {
    try {
      await db.run('DELETE FROM customers WHERE id = ?', [id]);
      return { success: true };
    } catch (error) {
      console.error('Error deleting customer:', error);
      return { success: false, error: error.message };
    }
  });
}

// Category handlers
function setupCategoryHandlers(ipcMain, db) {
  // Get all categories
  ipcMain.handle('get-categories', async () => {
    try {
      const categories = await db.all('SELECT * FROM categories ORDER BY name');
      return { success: true, data: categories };
    } catch (error) {
      console.error('Error getting categories:', error);
      return { success: false, error: error.message };
    }
  });

  // Add a new category
  ipcMain.handle('add-category', async (event, category) => {
    try {
      const result = await db.run(
        'INSERT INTO categories (name, description) VALUES (?, ?)',
        [category.name, category.description]
      );
      return { success: true, data: { id: result.lastID } };
    } catch (error) {
      console.error('Error adding category:', error);
      return { success: false, error: error.message };
    }
  });

  // Update a category
  ipcMain.handle('update-category', async (event, category) => {
    try {
      await db.run(
        'UPDATE categories SET name = ?, description = ? WHERE id = ?',
        [category.name, category.description, category.id]
      );
      return { success: true };
    } catch (error) {
      console.error('Error updating category:', error);
      return { success: false, error: error.message };
    }
  });

  // Delete a category
  ipcMain.handle('delete-category', async (event, id) => {
    try {
      await db.run('DELETE FROM categories WHERE id = ?', [id]);
      return { success: true };
    } catch (error) {
      console.error('Error deleting category:', error);
      return { success: false, error: error.message };
    }
  });
}

// Export the setup function
module.exports = (ipcMain, db) => {
  setupProductHandlers(ipcMain, db);
  setupSaleHandlers(ipcMain, db);
  setupCustomerHandlers(ipcMain, db);
  setupCategoryHandlers(ipcMain, db);
}; 