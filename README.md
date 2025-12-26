<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日用品買い忘れ防止アプリ</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Meiryo, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .header .subtitle {
            font-size: 14px;
            opacity: 0.9;
        }

        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
            overflow-x: auto;
        }

        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 14px;
            font-weight: bold;
            color: #6c757d;
            transition: all 0.3s;
            white-space: nowrap;
            min-width: 100px;
        }

        .tab.active {
            color: #667eea;
            background: white;
            border-bottom: 3px solid #667eea;
        }

        .tab:hover {
            background: #e9ecef;
        }

        .content {
            padding: 20px;
        }

        .section {
            display: none;
        }

        .section.active {
            display: block;
        }

        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }

        .card.danger {
            border-left-color: #dc3545;
            background: #fff5f5;
        }

        .card.warning {
            border-left-color: #ffc107;
            background: #fffef5;
        }

        .card.success {
            border-left-color: #28a745;
            background: #f5fff5;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #495057;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            font-size: 14px;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5568d3;
        }

        .btn-success {
            background: #28a745;
            color: white;
        }

        .btn-success:hover {
            background: #218838;
        }

        .btn-danger {
            background: #dc3545;
            color: white;
        }

        .btn-danger:hover {
            background: #c82333;
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
        }

        .btn-small {
            padding: 5px 10px;
            font-size: 12px;
        }

        .item-list {
            margin-top: 20px;
        }

        .item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }

        .item-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .item-name {
            font-size: 16px;
            font-weight: bold;
            color: #212529;
        }

        .item-details {
            font-size: 13px;
            color: #6c757d;
            margin-bottom: 5px;
        }

        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 5px;
        }

        .badge-danger {
            background: #dc3545;
            color: white;
        }

        .badge-warning {
            background: #ffc107;
            color: #212529;
        }

        .badge-success {
            background: #28a745;
            color: white;
        }

        .badge-info {
            background: #17a2b8;
            color: white;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-number {
            font-size: 32px;
            font-weight: bold;
        }

        .stat-label {
            font-size: 12px;
            opacity: 0.9;
            margin-top: 5px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #6c757d;
        }

        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 10px;
        }

        .data-management {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .history-item {
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .alert {
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 14px;
        }

        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 20px;
            }

            .tab {
                font-size: 12px;
                padding: 12px 8px;
                min-width: 80px;
            }

            .content {
                padding: 15px;
            }

            .stats {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media print {
            body {
                background: white;
            }
            .tabs, .btn, .data-management {
                display: none !important;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 日用品買い忘れ防止アプリ</h1>
            <div class="subtitle">買い物をスマートに管理</div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('dashboard')">
                📊 ダッシュボード
                <span id="dashboardBadge" class="badge badge-danger" style="display: none; margin-left: 5px;"></span>
            </button>
            <button class="tab" onclick="showTab('master')">📝 日用品マスター</button>
            <button class="tab" onclick="showTab('shopping')">🛍️ お買い物登録</button>
            <button class="tab" onclick="showTab('history')">📋 購入履歴</button>
            <button class="tab" onclick="showTab('data')">💾 データ管理</button>
        </div>

        <div class="content">
            <!-- ダッシュボード -->
            <div id="dashboard" class="section active">
                <div class="stats" id="statsContainer"></div>
                
                <div id="urgentAlert" class="alert" style="display: none; background: #fff3cd; border-left: 4px solid #ffc107; margin-bottom: 20px;">
                    <strong>⚠️ 購入が必要な商品があります！</strong>
                </div>
                
                <h3 style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                    🔥 今週の買い物リスト
                    <span id="weeklyBadge" class="badge badge-danger" style="display: none; font-size: 14px;"></span>
                </h3>
                <div id="shoppingList"></div>
                
                <h3 style="margin-bottom: 15px; margin-top: 30px;">✅ 購入済み・余裕あり</h3>
                <div id="okList"></div>
            </div>

            <!-- 日用品マスター -->
            <div id="master" class="section">
                <div class="card">
                    <h3 style="margin-bottom: 15px;">新規日用品登録</h3>
                    <div class="form-group">
                        <label>品名 *</label>
                        <input type="text" id="itemName" placeholder="例: ティッシュペーパー">
                    </div>
                    <div class="form-group">
                        <label>仕入れ周期（日数） *</label>
                        <input type="number" id="itemCycle" placeholder="例: 30" min="1">
                    </div>
                    <div class="form-group">
                        <label>カテゴリ</label>
                        <select id="itemCategory">
                            <option value="日用品">日用品</option>
                            <option value="食品">食品</option>
                            <option value="洗剤">洗剤</option>
                            <option value="トイレ用品">トイレ用品</option>
                            <option value="キッチン用品">キッチン用品</option>
                            <option value="その他">その他</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="addItem()">➕ 登録</button>
                </div>

                <div class="item-list" id="masterList"></div>
            </div>

            <!-- お買い物登録 -->
            <div id="shopping" class="section">
                <div class="card">
                    <h3 style="margin-bottom: 15px;">購入記録</h3>
                    <div class="form-group">
                        <label>商品選択 *</label>
                        <select id="purchaseItem">
                            <option value="">商品を選択してください</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>購入日 *</label>
                        <input type="date" id="purchaseDate">
                    </div>
                    <button class="btn btn-success" onclick="recordPurchase()">✅ 購入記録</button>
                </div>

                <div class="alert alert-info" style="margin-top: 20px;">
                    💡 購入した商品を記録すると、次回購入予定日が自動計算されます
                </div>
            </div>

            <!-- 購入履歴 -->
            <div id="history" class="section">
                <h3 style="margin-bottom: 15px;">📜 購入履歴</h3>
                <div id="historyList"></div>
            </div>

            <!-- データ管理 -->
            <div id="data" class="section">
                <div class="card">
                    <h3 style="margin-bottom: 15px;">データ管理</h3>
                    
                    <h4 style="margin: 15px 0 10px 0;">バックアップ</h4>
                    <div class="data-management">
                        <button class="btn btn-primary" onclick="exportData()">📥 データをエクスポート</button>
                        <button class="btn btn-secondary" onclick="printData()">🖨️ 印刷</button>
                    </div>

                    <h4 style="margin: 20px 0 10px 0;">データ復元</h4>
                    <div class="form-group">
                        <input type="file" id="importFile" accept=".json" style="margin-bottom: 10px;">
                        <button class="btn btn-success" onclick="importData()">📤 データをインポート</button>
                    </div>

                    <h4 style="margin: 20px 0 10px 0;">データ削除</h4>
                    <button class="btn btn-danger" onclick="clearAllData()">🗑️ 全データ削除</button>
                </div>

                <div class="card" style="margin-top: 20px;">
                    <h3 style="margin-bottom: 10px;">📊 データ統計</h3>
                    <div id="dataStats"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // データ構造
        let items = JSON.parse(localStorage.getItem('items')) || [];
        let purchases = JSON.parse(localStorage.getItem('purchases')) || [];

        // 初期化
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('purchaseDate').valueAsDate = new Date();
            loadData();
        });

        // タブ切り替え
        function showTab(tabName) {
            // 全セクション非表示
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // 全タブ非アクティブ
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // 選択されたセクションとタブをアクティブに
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');

            // データ再読み込み
            loadData();
        }

        // 日用品追加
        function addItem() {
            const name = document.getElementById('itemName').value.trim();
            const cycle = parseInt(document.getElementById('itemCycle').value);
            const category = document.getElementById('itemCategory').value;

            if (!name || !cycle) {
                alert('品名と仕入れ周期を入力してください');
                return;
            }

            const item = {
                id: Date.now(),
                name: name,
                cycle: cycle,
                category: category,
                createdAt: new Date().toISOString()
            };

            items.push(item);
            saveData();
            
            // フォームクリア
            document.getElementById('itemName').value = '';
            document.getElementById('itemCycle').value = '';
            
            loadData();
            alert('日用品を登録しました');
        }

        // 日用品削除
        function deleteItem(id) {
            if (!confirm('この日用品を削除しますか？')) return;
            
            items = items.filter(item => item.id !== id);
            purchases = purchases.filter(purchase => purchase.itemId !== id);
            saveData();
            loadData();
        }

        // 購入記録
        function recordPurchase() {
            const itemId = parseInt(document.getElementById('purchaseItem').value);
            const date = document.getElementById('purchaseDate').value;

            if (!itemId || !date) {
                alert('商品と購入日を選択してください');
                return;
            }

            const item = items.find(i => i.id === itemId);
            if (!item) return;

            const purchase = {
                id: Date.now(),
                itemId: itemId,
                itemName: item.name,
                purchaseDate: date,
                nextPurchaseDate: calculateNextDate(date, item.cycle)
            };

            purchases.push(purchase);
            saveData();
            loadData();
            
            alert(`${item.name}の購入を記録しました\n次回購入予定: ${formatDate(purchase.nextPurchaseDate)}`);
        }

        // 次回購入日計算
        function calculateNextDate(dateStr, cycle) {
            const date = new Date(dateStr);
            date.setDate(date.getDate() + cycle);
            return date.toISOString().split('T')[0];
        }

        // 日付フォーマット
        function formatDate(dateStr) {
            const date = new Date(dateStr);
            return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
        }

        // 日数差計算
        function getDaysDiff(dateStr) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const targetDate = new Date(dateStr);
            targetDate.setHours(0, 0, 0, 0);
            return Math.floor((targetDate - today) / (1000 * 60 * 60 * 24));
        }

        // データ保存
        function saveData() {
            localStorage.setItem('items', JSON.stringify(items));
            localStorage.setItem('purchases', JSON.stringify(purchases));
        }

        // データ読み込み
        function loadData() {
            loadMasterList();
            loadDashboard();
            loadPurchaseSelect();
            loadHistory();
            loadDataStats();
        }

        // マスターリスト表示
        function loadMasterList() {
            const container = document.getElementById('masterList');
            
            if (items.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📦</div>
                        <p>日用品が登録されていません</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = items.map(item => {
                const latestPurchase = purchases
                    .filter(p => p.itemId === item.id)
                    .sort((a, b) => new Date(b.purchaseDate) - new Date(a.purchaseDate))[0];

                return `
                    <div class="item">
                        <div class="item-header">
                            <div class="item-name">${item.name}</div>
                            <button class="btn btn-danger btn-small" onclick="deleteItem(${item.id})">削除</button>
                        </div>
                        <div class="item-details">
                            <span class="badge badge-info">${item.category}</span>
                            周期: ${item.cycle}日
                        </div>
                        ${latestPurchase ? `
                            <div class="item-details">
                                最終購入: ${formatDate(latestPurchase.purchaseDate)} | 
                                次回予定: ${formatDate(latestPurchase.nextPurchaseDate)}
                            </div>
                        ` : `
                            <div class="item-details" style="color: #dc3545;">
                                まだ購入記録がありません
                            </div>
                        `}
                    </div>
                `;
            }).join('');
        }

        // ダッシュボード表示
        function loadDashboard() {
            // 統計情報
            const statsContainer = document.getElementById('statsContainer');
            const itemsNeedToBuy = getItemsNeedToBuy();
            
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${items.length}</div>
                    <div class="stat-label">登録商品数</div>
                </div>
                <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="stat-number">${itemsNeedToBuy.urgent}</div>
                    <div class="stat-label">要購入（期限切れ）</div>
                </div>
                <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <div class="stat-number">${itemsNeedToBuy.soon}</div>
                    <div class="stat-label">今週中に購入</div>
                </div>
            `;

            // 通知バッジ更新
            const totalNeed = itemsNeedToBuy.urgent + itemsNeedToBuy.soon;
            const dashboardBadge = document.getElementById('dashboardBadge');
            const weeklyBadge = document.getElementById('weeklyBadge');
            
            if (totalNeed > 0) {
                dashboardBadge.style.display = 'inline-block';
                dashboardBadge.textContent = totalNeed;
                weeklyBadge.style.display = 'inline-block';
                weeklyBadge.textContent = `${totalNeed}件`;
                document.getElementById('urgentAlert').style.display = 'block';
            } else {
                dashboardBadge.style.display = 'none';
                weeklyBadge.style.display = 'none';
                document.getElementById('urgentAlert').style.display = 'none';
            }

            // 買い物リスト（1週間以内）
            const shoppingListContainer = document.getElementById('shoppingList');
            const allItems = generateShoppingList();
            const weeklyItems = allItems.filter(item => item.daysLeft <= 7);

            if (weeklyItems.length === 0) {
                shoppingListContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">✅</div>
                        <p>今週購入が必要な商品はありません</p>
                    </div>
                `;
            } else {
                // カテゴリ別にグループ化
                const categories = {
                    expired: weeklyItems.filter(item => item.daysLeft < 0),
                    today: weeklyItems.filter(item => item.daysLeft === 0),
                    threeDays: weeklyItems.filter(item => item.daysLeft > 0 && item.daysLeft <= 3),
                    week: weeklyItems.filter(item => item.daysLeft > 3 && item.daysLeft <= 7)
                };

                let html = '';

                // 期限切れ
                if (categories.expired.length > 0) {
                    html += `<div style="margin-bottom: 20px;">
                        <h4 style="color: #dc3545; margin-bottom: 10px;">🚨 期限切れ（${categories.expired.length}件）</h4>
                        ${renderItems(categories.expired, 'danger')}
                    </div>`;
                }

                // 今日
                if (categories.today.length > 0) {
                    html += `<div style="margin-bottom: 20px;">
                        <h4 style="color: #ff6b6b; margin-bottom: 10px;">📍 今日が期限（${categories.today.length}件）</h4>
                        ${renderItems(categories.today, 'danger')}
                    </div>`;
                }

                // 3日以内
                if (categories.threeDays.length > 0) {
                    html += `<div style="margin-bottom: 20px;">
                        <h4 style="color: #ffc107; margin-bottom: 10px;">⚡ 3日以内（${categories.threeDays.length}件）</h4>
                        ${renderItems(categories.threeDays, 'warning')}
                    </div>`;
                }

                // 1週間以内
                if (categories.week.length > 0) {
                    html += `<div style="margin-bottom: 20px;">
                        <h4 style="color: #28a745; margin-bottom: 10px;">📅 今週中（${categories.week.length}件）</h4>
                        ${renderItems(categories.week, 'success')}
                    </div>`;
                }

                shoppingListContainer.innerHTML = html;
            }

            // 余裕がある商品リスト
            const okListContainer = document.getElementById('okList');
            const okItems = allItems.filter(item => item.daysLeft > 7);
            
            if (okItems.length === 0) {
                okListContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📦</div>
                        <p>全ての商品が1週間以内に購入予定です</p>
                    </div>
                `;
            } else {
                okListContainer.innerHTML = okItems.map(item => `
                    <div class="item" style="opacity: 0.7;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: bold; font-size: 14px;">
                                    ${item.name}
                                    <span class="badge badge-info">${item.category}</span>
                                </div>
                                <div style="font-size: 12px; color: #6c757d; margin-top: 3px;">
                                    次回購入予定: ${formatDate(item.nextDate)} (あと${item.daysLeft}日)
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        }

        // アイテム表示用ヘルパー関数
        function renderItems(items, type) {
            return items.map(item => {
                let cardClass = 'card';
                let badge = '';
                let daysText = '';
                
                if (item.daysLeft < 0) {
                    cardClass = 'card danger';
                    badge = '<span class="badge badge-danger">期限切れ</span>';
                    daysText = `${Math.abs(item.daysLeft)}日経過`;
                } else if (item.daysLeft === 0) {
                    cardClass = 'card danger';
                    badge = '<span class="badge badge-danger">今日</span>';
                    daysText = '今日が期限';
                } else if (item.daysLeft <= 3) {
                    cardClass = 'card warning';
                    badge = '<span class="badge badge-warning">要注意</span>';
                    daysText = `あと${item.daysLeft}日`;
                } else if (item.daysLeft <= 7) {
                    cardClass = 'card success';
                    badge = '<span class="badge badge-success">今週中</span>';
                    daysText = `あと${item.daysLeft}日`;
                }

                return `
                    <div class="${cardClass}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">
                                    ${badge}
                                    ${item.name}
                                </div>
                                <div style="font-size: 13px; color: #6c757d;">
                                    <span class="badge badge-info">${item.category}</span>
                                    ${formatDate(item.nextDate)} (${daysText})
                                </div>
                            </div>
                            <div style="text-align: right; font-size: 24px; font-weight: bold; color: ${
                                item.daysLeft < 0 ? '#dc3545' : 
                                item.daysLeft === 0 ? '#dc3545' :
                                item.daysLeft <= 3 ? '#ffc107' : '#28a745'
                            };">
                                ${item.daysLeft < 0 ? '!' : item.daysLeft}
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        // 購入が必要な商品数を取得
        function getItemsNeedToBuy() {
            const list = generateShoppingList();
            return {
                urgent: list.filter(item => item.daysLeft < 0).length,
                soon: list.filter(item => item.daysLeft >= 0 && item.daysLeft <= 7).length
            };
        }

        // 買い物リスト生成
        function generateShoppingList() {
            const list = [];

            items.forEach(item => {
                const latestPurchase = purchases
                    .filter(p => p.itemId === item.id)
                    .sort((a, b) => new Date(b.purchaseDate) - new Date(a.purchaseDate))[0];

                if (latestPurchase) {
                    const daysLeft = getDaysDiff(latestPurchase.nextPurchaseDate);
                    list.push({
                        id: item.id,
                        name: item.name,
                        category: item.category,
                        nextDate: latestPurchase.nextPurchaseDate,
                        daysLeft: daysLeft
                    });
                } else {
                    // 購入記録がない場合も表示
                    list.push({
                        id: item.id,
                        name: item.name,
                        category: item.category,
                        nextDate: new Date().toISOString().split('T')[0],
                        daysLeft: 0
                    });
                }
            });

            // 日数でソート
            return list.sort((a, b) => a.daysLeft - b.daysLeft);
        }

        // 購入商品選択肢読み込み
        function loadPurchaseSelect() {
            const select = document.getElementById('purchaseItem');
            select.innerHTML = '<option value="">商品を選択してください</option>' + 
                items.map(item => `<option value="${item.id}">${item.name} (${item.category})</option>`).join('');
        }

        // 購入履歴表示
        function loadHistory() {
            const container = document.getElementById('historyList');
            
            if (purchases.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📋</div>
                        <p>購入履歴がありません</p>
                    </div>
                `;
                return;
            }

            const sortedPurchases = purchases.sort((a, b) => 
                new Date(b.purchaseDate) - new Date(a.purchaseDate)
            );

            container.innerHTML = sortedPurchases.map(purchase => `
                <div class="history-item">
                    <div>
                        <div style="font-weight: bold;">${purchase.itemName}</div>
                        <div style="font-size: 12px; color: #6c757d;">
                            購入日: ${formatDate(purchase.purchaseDate)} → 
                            次回予定: ${formatDate(purchase.nextPurchaseDate)}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // データ統計表示
        function loadDataStats() {
            const container = document.getElementById('dataStats');
            container.innerHTML = `
                <div style="line-height: 1.8;">
                    <p>📦 登録商品数: <strong>${items.length}</strong> 件</p>
                    <p>🛍️ 購入記録数: <strong>${purchases.length}</strong> 件</p>
                    <p>📅 最終更新: <strong>${new Date().toLocaleString('ja-JP')}</strong></p>
                </div>
            `;
        }

        // データエクスポート
        function exportData() {
            const data = {
                items: items,
                purchases: purchases,
                exportDate: new Date().toISOString()
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `shopping-data-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        // データインポート
        function importData() {
            const file = document.getElementById('importFile').files[0];
            if (!file) {
                alert('ファイルを選択してください');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (confirm('現在のデータを上書きしますか？')) {
                        items = data.items || [];
                        purchases = data.purchases || [];
                        saveData();
                        loadData();
                        alert('データをインポートしました');
                    }
                } catch (error) {
                    alert('ファイルの読み込みに失敗しました');
                }
            };
            reader.readAsText(file);
        }

        // 全データ削除
        function clearAllData() {
            if (!confirm('本当に全データを削除しますか？この操作は取り消せません。')) return;
            if (!confirm('最終確認：全データを削除します。よろしいですか？')) return;

            items = [];
            purchases = [];
            saveData();
            loadData();
            alert('全データを削除しました');
        }

        // 印刷
        function printData() {
            window.print();
        }
    </script>
</body>
</html>
