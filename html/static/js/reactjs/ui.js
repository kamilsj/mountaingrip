'use strict';

const e = React.createElement;
const dom = document.querySelector('#suggestions');

class Autocompletion extends React.Component {
  constructor(props){
    super(props);
  }
  componentDidMount() {
    fetch('/api/autocomplete')
  }
}

class Suggestions extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      error: null,
      isLoaded: false,
      groups: [],
      posts: [],
      users: []
    };
  }
  
  componentDidMount(){
    fetch("/api/suggestions")
    .then(res=> res.json())
    .then(
      (result) => {
        this.setState({
          isLoaded: true,
          groups: result.groups,
          posts: result.posts,
          users: result.users
        });
      },
      (error) => {
        this.setState({
          isLoaded: true,
          error
        });
      }
    )
  }

  render() {
    const { error, isLoaded, groups } = this.state;
    if (error) {
      return e('div', {class: 'alert alert-danger'}, "Error: ", error.message);
    } else if(!isLoaded) {
      return e('div', {class: 'spinner-border', role: 'status'}, e('span', {class: 'sr-only'}, 'Loading...'));
    } else {
      return e('ul', {class: 'list-group'}, groups.map(group => (
        e('li', {class: 'list-group-item'}, group.id)
      )))
    }
  }
}


ReactDOM.render(e(Suggestions), dom);