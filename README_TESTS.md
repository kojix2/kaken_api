# KAKEN API クライアントライブラリのテスト

このドキュメントでは、KAKEN APIクライアントライブラリのテスト方法について説明します。

## 前提条件

テストを実行するには、以下のパッケージが必要です：

```bash
pip install pytest pytest-cov
```

## 環境変数の設定

テストを実行する前に、KAKEN APIのアプリケーションIDを環境変数に設定する必要があります：

```bash
# Linux/macOS
export KAKEN_APP_ID=your_app_id

# Windows
set KAKEN_APP_ID=your_app_id
```

アプリケーションIDは、[CiNii全般 - メタデータ・API - API利用登録](https://support.nii.ac.jp/ja/cinii/api/developer) から取得できます。

## テストの実行

### すべてのテストを実行

```bash
pytest
```

### 特定のテストファイルを実行

```bash
pytest tests/test_utils.py
```

### 特定のテスト関数を実行

```bash
pytest tests/test_utils.py::test_build_url
```

### カバレッジレポートを生成

```bash
pytest --cov=kaken_api
```

HTMLカバレッジレポートを生成する場合：

```bash
pytest --cov=kaken_api --cov-report=html
```

## 注意事項

1. **API呼び出し回数**: すべてのテストで実際のAPIを呼び出すため、APIのレート制限に注意してください。
2. **テスト実行時間**: APIリクエストを伴うため、テストの実行時間が長くなる可能性があります。
3. **テストの安定性**: APIの状態やネットワーク状況によってテスト結果が変わる可能性があります。
4. **アサーション**: 具体的な値ではなく、型や存在確認などの一般的なアサーションを使用しています。

## テストの構造

- `tests/conftest.py`: テスト用のフィクスチャを定義
- `tests/test_utils.py`: ユーティリティ関数のテスト
- `tests/test_client.py`: クライアントクラスのテスト
- `tests/test_projects_api.py`: プロジェクト検索APIのテスト
- `tests/test_researchers_api.py`: 研究者検索APIのテスト
