import { Card, Popup, Icon, Grid, Image, Button } from "semantic-ui-react";
import { useState } from "react";

export default function ChatWindow() {
    const [showChat, setShowChat] = useState(false)

    if (!showChat) {
        return (
            <div className='chat-window'>
                <Popup

                    trigger={
                        <Card
                            style={{ height: '3vw', width: '25vw', textAlign: 'left', padding: '5%' }}
                            onClick={() => setShowChat(true)}
                        >
                        </Card>
                    }
                    content='Chat with us!'
                    position='top right'
                    basic
                />
                
            </div>

        )
    }


    return (
        <div className='chat-window'>
            
            <Card
                style={{ height: '25vw', width: '25vw', textAlign: 'left', padding: '4%' }}
            >
                {/* <Grid>
                    <Grid.Row color='blue'>
                        <Grid.Column width={14}>
                        </Grid.Column>
                        
                    </Grid.Row>
                        <p>TODO: Build a chat window!</p>
                    <Grid.Row>
                        
                    </Grid.Row>
                </Grid> */}
                <Card.Header >
                    <Button icon='x' onClick={() => setShowChat(false)}/> 
                </Card.Header>

            </Card>
        </div>
    )
}

