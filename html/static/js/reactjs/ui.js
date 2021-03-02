'use strict';

const e = React.createElement;

class Suggestions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        }
    }
    componentDidMount() {
        fetch('/api/suggestions/')
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result.items
                    });
                }
            )
    }
    render() {
        const { error, items, isLoaded } = this.state;
        if (error){
            return e('div', null, error.message);
        } else if (!isLoaded) {
            return e('div', null, 'Loading');
        } else {
            return items;
        }
    }
}

ReactDOM.render(
    e('div', null, e('ul', null, items.map(item => e('li', null, item)))),
  document.getElementById('suggestions')
    );