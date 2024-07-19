import React from "react";
import Button from "../../../generic/Button";
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

const Article = ({ article, onDelete }) => {
  async function deleteArticleFromServer(article) {
    await axios.delete("http://127.0.0.1:8000/api/v1/articles/" + article.id);
  }

  return (
    <div className={styles.article}>
      <h3>{article.title}</h3>
      <p>{article.content}</p>
      <div>
        <Button text="Delete" onClick={async () => {
          deleteArticleFromServer(article);
          onDelete(article);
        }} />
        <span>{formatDate(article.created_at)}</span>
      </div>
    </div>
  );
};

export default Article;
