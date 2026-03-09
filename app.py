from flask import Flask, render_template, request, redirect, url_for
import json
import os

# 创建Flask应用实例
app = Flask(__name__)

class WarehouseManager:
    """仓库管理类，负责商品数据的增删改查操作"""
    
    def __init__(self):
        """初始化仓库管理器，加载数据"""
        self.data_file = 'warehouse_data.json'  # 数据存储文件
        self.items = self.load_data()  # 加载现有数据
    
    def load_data(self):
        """从JSON文件加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []  # 如果文件不存在，返回空列表
    
    def save_data(self):
        """将数据保存到JSON文件"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
    
    def add_item(self, name, quantity, category):
        """添加新商品
        
        Args:
            name: 商品名称
            quantity: 商品数量
            category: 商品分类
            
        Returns:
            新添加的商品对象
        """
        item = {
            'id': len(self.items) + 1,  # 自动生成ID
            'name': name,
            'quantity': quantity,
            'category': category
        }
        self.items.append(item)
        self.save_data()
        return item
    
    def get_all_items(self):
        """获取所有商品"""
        return self.items
    
    def get_item_by_id(self, item_id):
        """根据ID获取商品
        
        Args:
            item_id: 商品ID
            
        Returns:
            商品对象，如果不存在返回None
        """
        for item in self.items:
            if item['id'] == item_id:
                return item
        return None
    
    def update_item(self, item_id, name, quantity, category):
        """更新商品信息
        
        Args:
            item_id: 商品ID
            name: 新商品名称
            quantity: 新商品数量
            category: 新商品分类
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        for item in self.items:
            if item['id'] == item_id:
                item['name'] = name
                item['quantity'] = quantity
                item['category'] = category
                self.save_data()
                return True
        return False
    
    def delete_item(self, item_id):
        """删除商品
        
        Args:
            item_id: 商品ID
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        for i, item in enumerate(self.items):
            if item['id'] == item_id:
                self.items.pop(i)
                self.save_data()
                return True
        return False
    
    def search_items(self, keyword):
        """搜索商品
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            list: 匹配的商品列表
        """
        results = []
        for item in self.items:
            if keyword.lower() in item['name'].lower() or keyword.lower() in item['category'].lower():
                results.append(item)
        return results

# 创建仓库管理器实例
manager = WarehouseManager()

@app.route('/')
def index():
    """首页路由，显示商品列表和统计信息"""
    items = manager.get_all_items()
    
    # 计算库存总量
    total_quantity = sum(item['quantity'] for item in items)
    
    # 计算分类数量
    categories = set()
    for item in items:
        categories.add(item['category'])
    category_count = len(categories)
    
    return render_template('index.html', items=items, total_quantity=total_quantity, category_count=category_count)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """添加商品路由"""
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        manager.add_item(name, quantity, category)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    """更新商品路由"""
    item = manager.get_item_by_id(item_id)
    if not item:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        manager.update_item(item_id, name, quantity, category)
        return redirect(url_for('index'))
    
    return render_template('update.html', item=item)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    """删除商品路由"""
    manager.delete_item(item_id)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """搜索商品路由"""
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = manager.search_items(keyword)
        return render_template('search.html', results=results, keyword=keyword)
    return render_template('search.html')

@app.route('/update-order', methods=['POST'])
def update_order():
    """更新商品顺序路由，用于拖拽排序功能"""
    data = request.get_json()
    item_ids = data.get('item_ids', [])
    
    # 更新商品顺序
    new_items = []
    for i, item_id in enumerate(item_ids, 1):
        for item in manager.items:
            if item['id'] == item_id:
                item['id'] = i  # 更新ID为新的顺序
                new_items.append(item)
                break
    
    manager.items = new_items
    manager.save_data()
    
    return {'success': True}

if __name__ == '__main__':
    """运行应用"""
    app.run(debug=True, host='0.0.0.0', port=5000)
