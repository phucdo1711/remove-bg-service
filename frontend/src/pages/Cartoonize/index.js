import React, { Fragment, useEffect, useState, useCallback } from "react";
import { Button, Card, Col, Row } from "antd";
import {
  LoadingOutlined,
  PlusOutlined,
  InboxOutlined,
  DownloadOutlined,
} from "@ant-design/icons";
import styles from "./Cartoonize.module.scss";
import axios from "utils/axios";
import { useDropzone } from "react-dropzone";

function getBase64(img, callback) {
  const reader = new FileReader();
  reader.addEventListener("load", () => callback(reader.result));
  reader.readAsDataURL(img);
}

const Cartoonize = () => {
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [file, setFile] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    // Do something with the files
    const file = acceptedFiles[0];
    if (!file) return;

    getBase64(file, setImageUrl);
    setFile(file);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    accept: "image/*",
    maxFiles: 1,
  });

  const uploadButton = (
    <div>
      {loading ? (
        <LoadingOutlined />
      ) : (
        <Fragment>
          <p className="ant-upload-drag-icon" style={{ marginBottom: 24 }}>
            <InboxOutlined style={{ fontSize: 64, color: "#1890ff" }} />
          </p>
          <p className="ant-upload-text">
            Click or drag file to this area to upload
          </p>
          <p className="ant-upload-hint">
            Support for a single or bulk upload. Strictly prohibit from
            uploading company data or other band files
          </p>
        </Fragment>
      )}
    </div>
  );

  return (
    <div>
      <Row>
        <Col sm={24} md={12} className={styles.col}>
          <div className={styles.uploadWrapper}>
            <div {...getRootProps()} className={styles.avatarUploader}>
              <input {...getInputProps()} />
              {imageUrl ? (
                <img
                  src={imageUrl}
                  alt="avatar"
                  style={{ maxWidth: "100%", maxHeight: "100%" }}
                />
              ) : (
                uploadButton
              )}
            </div>
          </div>
        </Col>
        {file && (
          <Col sm={24} md={12} className={styles.col}>
            <ResultImage
              file={file}
              uploadFnc={async (file) => {
                const formData = new FormData();
                formData.append("file", file);
                const res = await axios.post(
                  "/api/cartoonize",
                  formData,
                  {
                    headers: {
                      "content-type": "multipart/form-data",
                    },
                    responseType: "arraybuffer",
                  }
                );
                return Buffer.from(res.data, "binary").toString("base64");
              }}
              title="Cartoonize"
            />
          </Col>
        )}
      </Row>
    </div>
  );
};

const ResultImage = ({ uploadFnc, file, title }) => {
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  useEffect(() => {
    setImageUrl("");
    const main = async () => {
      setLoading(true);
      try {
        const buffer = await uploadFnc(file);
        setImageUrl("data:image/png;base64," + buffer);
      } catch (error) {
        alert(error.message)
      }
      setLoading(false);
    };
    main();
  }, [file]);
  const download = () => {
    window.location.href = imageUrl;
    var a = document.createElement("a"); //Create <a>
    a.href = imageUrl; //Image Base64 Goes here
    a.download = `image-result.png`; //File name Here
    a.click();
  };

  return (
    <Card
      title={title}
      extra={
        imageUrl && (
          <Button
            type="primary"
            shape="round"
            icon={<DownloadOutlined />}
            onClick={download}
          />
        )
      }
      style={{ marginBottom: 16 }}
    >
      {loading || !imageUrl ? (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <LoadingOutlined style={{ fontSize: 32 }} />
        </div>
      ) : (
        <img src={imageUrl} style={{ maxWidth: "100%" }} />
      )}
    </Card>
  );
};

export default Cartoonize;
