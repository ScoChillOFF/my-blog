import React, { useState } from "react";
import Button from "../../../generic/Button";
import TextInput from "../../../generic/TextInput";
import TextArea from "../../../generic/TextArea";
import axios from "axios";
import styles from "./Article.module.css";

function formatDate(strDateTime) {
  const date = new Date(strDateTime);

  const dateOptions = {
    day: "2-digit",
    month: "short",
    year: "numeric",
  };

  const timeOptions = {
    hour: "2-digit",
    minute: "2-digit",
  };

  const time = date.toLocaleTimeString("en-US", timeOptions);

  const formattedDate = date.toLocaleDateString("en-US", dateOptions);

  return `${time} ${formattedDate}`;
}

const Article = ({ article, onDelete, onUpdate }) => {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(article.title);
  const [content, setContent] = useState(article.content);
  const isReadyToSubmit = title.length != 0 && content.length != 0;

  async function deleteArticleFromServer(article) {
    await axios.delete("http://127.0.0.1:8000/api/v1/articles/" + article.id);
  }

  async function updateArticleOnServer() {
    const fieldsUpdate = {
      title: title,
      content: content,
    };
    const response = await axios.put(
      "http://127.0.0.1:8000/api/v1/articles/" + article.id,
      fieldsUpdate
    );
    const updatedArticle = response.data;
    return updatedArticle;
  }

  if (editing) {
    return (
      <div className={styles.article}>
        <TextInput jsonField="title" onChange={setTitle} value={title} />
        <TextArea jsonField="content" onChange={setContent} value={content} />
        <div>
          <div className={styles.buttons}>
            <Button
              text="Submit"
              disabled={!isReadyToSubmit}
              onClick={async () => {
                const updatedArticle = await updateArticleOnServer();
                onUpdate(updatedArticle);
                setEditing(false);
              }}
            />
            <Button
              text="Cancel"
              onClick={() => {
                setEditing(false);
                setTitle(article.title);
                setContent(article.content);
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.article}>
      <h3>{article.title}</h3>
      <p>{article.content}</p>
      <div>
        <div className={styles.buttons}>
          <Button
            text="Delete"
            onClick={async () => {
              deleteArticleFromServer(article);
              onDelete(article);
            }}
          />
          <Button text="Edit" onClick={() => setEditing(true)} />
        </div>
        <span>{formatDate(article.created_at)}</span>
      </div>
    </div>
  );
};

export default Article;
