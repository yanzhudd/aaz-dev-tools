import React, { useState } from "react";
import ArrowRightIcon from "@mui/icons-material/ArrowRight";
import { NodeModel, useDragOver } from "@minoru/react-dnd-treeview";
import { CustomData } from "./types";
import { TypeIcon } from "./TypeIcon";
import IconButton from "@mui/material/IconButton";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import styles from "./CustomNode.module.css";


type Props = {
  node: NodeModel<CustomData>;
  depth: number;
  isOpen: boolean;
  isSelected: boolean;
  onToggle: (id: NodeModel["id"]) => void;
  onClick: (id: NodeModel["id"]) => void
  onSubmit: (id: NodeModel["id"], newName: string) => void
};

export const CustomNode: React.FC<Props> = (props) => {
  const { id, droppable, data, text } = props.node;
  const indent = props.depth * 12;

  const [editing, setEditing] = useState(false)
  const [nodeName, setNodeName] = useState(text)
  const [changingName, setChangingName] = useState(nodeName)

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    props.onToggle(id);
  };

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    props.onClick(id);
  }

  const handleDoubleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!editing) {
      setEditing(true)
      setChangingName(nodeName)
    }

  }

  const handleChangeName = (event: any) => {
    setChangingName(event.target.value)
  }

  const handleSubmit = (event: any) => {
    setEditing(false)
    setNodeName(changingName.trim())
    props.onSubmit(id, changingName.trim())
  }

  const handleCancel = (event: any) => {
    setEditing(false)
    setChangingName(nodeName)
  }

  const dragOverProps = useDragOver(id, props.isOpen, props.onToggle);

  return (
    <div
      className={`tree-node ${styles.root} ${props.isSelected ? styles.isSelected : ""}`}
      style={{ paddingInlineStart: indent, whiteSpace: `nowrap`}}
      {...dragOverProps}
      onClick={handleClick}
    >
      {droppable && data?.hasChildren && (<div className={`${styles.expandIconWrapper} ${props.isOpen ? styles.isOpen : ""}`} onClick={handleToggle}>
        {(
          <div >
            <ArrowRightIcon />
          </div>
        )}
      </div>)}
      <div>
        <TypeIcon type={data?.type} />
      </div>
      <div className={styles.labelGridItem} onDoubleClick={handleDoubleClick}>
        {!editing ? nodeName :
          (
            <div className={styles.inputWrapper}>
              <input style={{ width: `${Math.max(20, changingName.length)}ch` }}
                value={changingName}
                onChange={handleChangeName}></input>
              <IconButton
                className={styles.editButton}
                onClick={handleSubmit}
                disabled={changingName === ""}
              >
                <CheckIcon className={styles.editIcon} />
              </IconButton>
              <IconButton className={styles.editButton} onClick={handleCancel}>
                <CloseIcon className={styles.editIcon} />
              </IconButton>
            </div>
          )
        }
      </div>
    </div>
  );
};
