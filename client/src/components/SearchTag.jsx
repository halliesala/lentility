export default function SearchTag({ tag, removeTag }) {

    
    return (
        <>
            <button key={tag}>{tag}</button>
            <button onClick={() => removeTag(tag)}>x</button>
        </>
    )
}