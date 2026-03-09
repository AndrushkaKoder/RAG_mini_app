<h1>Мини приложение для Retrieval-Augmented Generation по книгам</h1>

<p>Приложение создает эмбединги из файлов в директории <strong>storage/</strong> и добавляет их в вектоную БД Qdrant</p>
<p>При запросе <strong>/api/query</strong> ответ llm (Qwen2.5) будет расширен контекстом из Qdrant</p>