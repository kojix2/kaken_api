KAKEN API Client Library for Python
================================

.. note::
   このライブラリは VSCode Cline `Anthropic Claude 3.7 Sonnet <https://www.anthropic.com/claude>`_ によって作成されています。

KAKEN API（科研費API）のPythonクライアントライブラリです。このライブラリを使用すると、科研費の研究課題や研究者の情報を簡単に検索・取得することができます。

インストール
----------

.. code-block:: bash

   pip install kaken_api

使用方法
-------

初期化
^^^^^

.. code-block:: python

   from kaken_api import KakenApiClient

   # アプリケーションIDを指定して初期化
   client = KakenApiClient(app_id="your_app_id")

   # または、アプリケーションIDなしで初期化（一部の機能が制限される場合があります）
   client = KakenApiClient()

   # キャッシュを無効化して初期化
   client = KakenApiClient(use_cache=False)

   # カスタムキャッシュディレクトリを指定して初期化
   client = KakenApiClient(cache_dir="/path/to/cache")

キャッシュ機能
^^^^^^^^^^^

このライブラリには、APIリクエストの結果をキャッシュする機能が組み込まれています。これにより、同じリクエストを繰り返し行う場合に、APIサーバーへの負荷を軽減し、レスポンス時間を短縮することができます。

キャッシュはデフォルトで有効になっており、``~/.kaken_api_cache``ディレクトリに保存されます。キャッシュを無効化したり、カスタムキャッシュディレクトリを指定したりすることもできます。

.. code-block:: python

   # キャッシュを無効化
   client = KakenApiClient(use_cache=False)

   # カスタムキャッシュディレクトリを指定
   client = KakenApiClient(cache_dir="/path/to/cache")

   # キャッシュをクリア
   client.cache.clear()

研究課題の検索
^^^^^^^^^^^

.. code-block:: python

   # キーワードで検索
   projects = client.projects.search(keyword="人工知能")

   # 詳細な検索条件を指定
   projects = client.projects.search(
       project_title="深層学習",
       research_category="基盤研究",
       grant_period_from=2020,
       grant_period_to=2023,
       results_per_page=50,
       language="ja",
   )

   # 検索結果の処理
   print(f"検索結果: {projects.total_results}件")
   for project in projects.projects:
       print(f"課題番号: {project.award_number}")
       print(f"課題名: {project.title}")
       print("---")

研究者の検索
^^^^^^^^^^

.. code-block:: python

   # キーワードで検索
   researchers = client.researchers.search(keyword="田中")

   # 詳細な検索条件を指定
   researchers = client.researchers.search(
       researcher_name="田中",
       researcher_institution="東京大学",
       results_per_page=50,
       language="ja",
   )

   # 検索結果の処理
   print(f"検索結果: {researchers.total_results}件")
   for researcher in researchers.researchers:
       if researcher.name:
           print(f"研究者名: {researcher.name.full_name}")
       for affiliation in researcher.affiliations:
           if affiliation.institution:
               print(f"所属機関: {affiliation.institution.name}")
           if affiliation.department:
               print(f"部局: {affiliation.department.name}")
           if affiliation.job_title:
               print(f"職名: {affiliation.job_title.name}")
       print("---")

アプリケーションIDの取得
-------------------

KAKEN APIを利用するには、CiNiiのアプリケーションIDが必要です。以下の手順で取得してください。

1. `CiNii全般 - メタデータ・API - API利用登録 <https://support.nii.ac.jp/ja/cinii/api/developer>`_ のページにアクセスします。
2. 「API利用登録」のリンクをクリックし、必要事項を入力して登録します。
3. 登録が完了すると、アプリケーションIDが発行されます。

API リファレンス
--------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/modules

インデックス
--------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
