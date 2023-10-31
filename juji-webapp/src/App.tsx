import './App.scss'
import {Button, ButtonGroup, Divider, Flex} from "monday-ui-react-core";
import { Heading } from "monday-ui-react-core/next";

function App() {
    const options = [
        {
            text: "Accueil",
            value: 1
        },
        {
            text: "Textes",
            value: 2
        },
        {
            text: "Evénementiels",
            value: 3
        },
        {
            text: "Discussions",
            value: 4
        },
        {
            text: "Gestion",
            value: 5
        },
        {
            text: "Membres",
            value: 6
        }
    ]
    return (
        <>
            <Flex direction={Flex.directions.COLUMN}>
                <Flex align={Flex.align.CENTER} justify={Flex.justify.SPACE_AROUND} style={{
                    width: "100%"
                }} wrap={true}>
                    <Heading>
                        Le Monde des Mots
                    </Heading>
                        <ButtonGroup options={options} kind={ButtonGroup.kinds.TERTIARY}></ButtonGroup>
                    <div>
                        <Button size={Button.sizes.SMALL}>Connexion</Button>
                        <Button size={Button.sizes.SMALL}>S'inscrire</Button>
                    </div>

                </Flex>
                <Divider></Divider>

            </Flex>
        </>
    )
}

export default App
